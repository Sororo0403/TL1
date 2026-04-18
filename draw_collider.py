import bpy
import gpu
import gpu_extras.batch
from mathutils import Vector


class DrawCollider:
    handle = None

    @staticmethod
    def draw_collider():
        vertices = {"pos": []}
        indices = []

        offsets = [
            (-0.5, -0.5, -0.5),
            (0.5, -0.5, -0.5),
            (-0.5, 0.5, -0.5),
            (0.5, 0.5, -0.5),
            (-0.5, -0.5, 0.5),
            (0.5, -0.5, 0.5),
            (-0.5, 0.5, 0.5),
            (0.5, 0.5, 0.5),
        ]

        for obj in bpy.context.scene.objects:
            if "collider" not in obj:
                continue

            start = len(vertices["pos"])
            center = obj["collider_center"]
            size = obj["collider_size"]

            for offset in offsets:
                pos = Vector(center)
                pos.x += offset[0] * size[0]
                pos.y += offset[1] * size[1]
                pos.z += offset[2] * size[2]
                pos = obj.matrix_world @ pos
                vertices["pos"].append(pos)

            edges = [
                (0, 1),
                (2, 3),
                (0, 2),
                (1, 3),
                (4, 5),
                (6, 7),
                (4, 6),
                (5, 7),
                (0, 4),
                (1, 5),
                (2, 6),
                (3, 7),
            ]

            for e in edges:
                indices.append((start + e[0], start + e[1]))

        if not vertices["pos"]:
            return

        shader = gpu.shader.from_builtin("UNIFORM_COLOR")
        batch = gpu_extras.batch.batch_for_shader(
            shader, "LINES", vertices, indices=indices
        )

        shader.bind()
        shader.uniform_float("color", (0.2, 0.8, 1.0, 1.0))
        batch.draw(shader)
