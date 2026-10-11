"""Generate honest neutral Blender image views for a human/multimodal critic.

Usage:
  blender --background model.blend --python scripts/render_review.py -- --output-dir outputs/previews
  blender --background model.blend --python scripts/render_review.py -- --output-dir outputs/previews --engine workbench --size 640

The script doesn't save modifications to the .blend. Render previews are NOT proof of artistic quality.
"""
import argparse
import json
import sys
from pathlib import Path

try:
    import bpy
    from mathutils import Vector
except ImportError as exc:
    raise SystemExit('Must run with Blender Python.') from exc


def parse_args():
    raw = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
    parser = argparse.ArgumentParser(description='Render inspection views')
    parser.add_argument('--output-dir', required=True)
    parser.add_argument('--engine', choices=['workbench', 'eevee'], default='workbench')
    parser.add_argument('--size', type=int, default=640)
    return parser.parse_args(raw)


def bounding_box_world():
    corners = []
    for obj in bpy.context.scene.objects:
        if obj.type != 'MESH' or obj.hide_render:
            continue
        corners.extend([obj.matrix_world @ Vector(v) for v in obj.bound_box])
    if not corners:
        raise ValueError('Cannot render: scene contains no visible mesh objects')
    mins = Vector(tuple(min(v[axis] for v in corners) for axis in range(3)))
    maxs = Vector(tuple(max(v[axis] for v in corners) for axis in range(3)))
    center = (mins + maxs) * 0.5
    dims = maxs - mins
    return mins, maxs, center, dims


def look_at(camera, target):
    camera.rotation_euler = (target - camera.location).to_track_quat('-Z', 'Y').to_euler()


def configure_renderer(engine):
    scene = bpy.context.scene
    if engine == 'workbench':
        scene.render.engine = 'BLENDER_WORKBENCH'
        scene.display.shading.light = 'STUDIO'
        scene.display.shading.color_type = 'MATERIAL'
        scene.display.shading.show_shadows = True
        scene.display.shading.show_cavity = True
    else:
        choices = [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items]
        available = [v for v in ('BLENDER_EEVEE_NEXT', 'BLENDER_EEVEE') if v in choices]
        if not available:
            raise RuntimeError('EEVEE engine not available; retry --engine workbench')
        scene.render.engine = available[0]
        # Use existing scene lights/materials in eevee. The caller should configure them.
    scene.render.image_settings.file_format = 'PNG'
    scene.render.film_transparent = False


def main():
    args = parse_args()
    if args.size < 128 or args.size > 4096:
        raise ValueError('Image size must be in [128, 4096]')
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    mins, maxs, center, dims = bounding_box_world()
    configure_renderer(args.engine)
    scene = bpy.context.scene
    scene.render.resolution_x = args.size
    scene.render.resolution_y = args.size
    scene.render.resolution_percentage = 100

    camera_data = bpy.data.cameras.new('REVIEW_CAMERA_DATA')
    camera = bpy.data.objects.new('REVIEW_CAMERA', camera_data)
    scene.collection.objects.link(camera)
    camera_data.type = 'ORTHO'
    scene.camera = camera
    height = max(float(dims.z), 0.2)
    size = max(float(dims.x), float(dims.y), height) * 1.35
    # Front convention is negative Y in a default VRM-style world; adjust if actual base differs.
    views = {
        'front': ((0, -1, 0.10), center, size),
        'three_quarter': ((0.80, -1, 0.15), center, size),
        'side': ((1, 0, 0.10), center, size),
        'back': ((0, 1, 0.10), center, size),
        'face_close': ((0, -1, 0.10), Vector((center.x, center.y, mins.z + 0.79 * height)), max(0.22, height * 0.53)),
    }
    generated=[]
    for name, (direction, target, ortho) in views.items():
        direction_vec = Vector(direction).normalized()
        camera.location = target + direction_vec * (size * 2.8)
        look_at(camera, target)
        camera_data.ortho_scale = ortho
        scene.render.filepath = str((out / f'{name}.png').resolve())
        bpy.ops.render.render(write_still=True)
        if not Path(scene.render.filepath).is_file():
            raise IOError(f'Expected render does not exist: {scene.render.filepath}')
        generated.append(scene.render.filepath)
        print('RENDER_WRITTEN:', scene.render.filepath)
    # Do not save the working .blend after temporary camera additions.
    manifest = {'blend_file': bpy.data.filepath or 'UNSAVED', 'engine': args.engine,
                'blender_version': bpy.app.version_string, 'renders': generated,
                'aesthetic_approval': 'NOT_TESTED', 'actual_reference_comparison': 'NOT_TESTED'}
    (out / 'preview_manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    print('PREVIEW_MANIFEST_WRITTEN:', str((out/'preview_manifest.json').resolve()))


if __name__ == '__main__':
    main()
