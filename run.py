import os 
import argparse 
# import open3d as o3d
import numpy as np
from colmap_utils import run_sfm, run_dense, run_geo_registration

# def cluster_and_compute_obbs(ply_path, voxel_size=0.01, eps=0.05, min_points=30):
#     pc = o3d.io.read_point_cloud(ply_path)
#     pc = pc.voxel_down_sample(voxel_size)
#     labels = np.array(
#         pc.cluster_dbscan(eps=eps, min_points=min_points, print_progress=True)
#     )
#     max_label = labels.max()
#     obbs = []
#     clusters = []
#     for i in range(max_label + 1):
#         idx = np.where(labels == i)[0].tolist()
#         if len(idx) < min_points:
#             continue
#         sub = pc.select_by_index(idx)
#         obb = sub.get_oriented_bounding_box()
#         obbs.append(obb)
#         clusters.append(sub)
#     return pc, clusters, obbs

# def compute_and_show(ply_path, voxel_size=0.01):
#     print(f"Loading {ply_path} ...")
#     pc = o3d.io.read_point_cloud(ply_path)
#     pc = pc.voxel_down_sample(voxel_size)
#     obb = pc.get_oriented_bounding_box()
#     dx, dy, dz = obb.extent
#     print(f"Bounding box (m): dx={dx:.3f}, dy={dy:.3f}, dz={dz:.3f}")

#     pc.paint_uniform_color([0.0, 1.0, 0.0])
#     obb.color = [1.0, 0.0, 0.0]
#     o3d.visualization.draw_geometries([pc, obb])

def main(args):
    os.makedirs("project", exist_ok=True)
    run_sfm(args.images, 'project/database.db', "project/sparse")
    run_geo_registration('project/sparse/0', 'project/sparse_georef', 'project/database.db')
    run_dense(args.images, 'project/sparse_georef', 'project/dense_georef')

    # ply = os.path.join('project/dense_georef', 'fused.ply')
    # # compute_and_show(ply, voxel_size=args.voxel_size)

    # pc, clusters, obbs = cluster_and_compute_obbs(ply_path=ply, 
    #                                               voxel_size=args.voxel_size,
    #                                               eps=args.eps,
    #                                               min_points=args.min_points)
    # print(f"Finded {len(obbs)} objects")
    # for i, obb in enumerate(obbs):
    #     dx, dy, dz = obb.extent
    #     print(f"Object {i}: dx={dx:.3f}, dy={dy:.3f}, dz={dz:.3f} (m)")

    # # Visualize
    # # pc.paint_uniform_color([0, 1.0, 0])
    # for i, cl in enumerate(clusters):
    #     cl.paint_uniform_color([np.random.rand(), np.random.rand(), np.random.rand()])
    # for obb in obbs:
    #     obb.color = (1.0, 0, 0)
    # o3d.visualization.draw_geometries([pc])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='SfM + Dense + OBB visualization')
    parser.add_argument('--images', type=str, default='images', help='Folder UAV image')
    parser.add_argument('--voxel_size', type=float, default=0.2, help='Voxel size (m)')
    parser.add_argument('--eps', type=float, default=2.0)
    parser.add_argument('--min_points', type=int, default=30)
    args = parser.parse_args()
    main(args)
