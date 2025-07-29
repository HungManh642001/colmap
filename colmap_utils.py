import os, sys, subprocess

os.environ['OPEN3D_RENDER_BACKEND'] = 'FILAMENT'

def resource_path(rel):
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, rel)
    return os.path.join(os.path.abspath("."), rel)

def run_colmap(step, args):
    exe = resource_path(os.path.join('colmap', 'COLMAP.bat'))
    cmd = [exe, step] + args
    subprocess.run(cmd, check=True, shell=True)


def run_sfm(image_dir, db_path, sparse_dir):
    os.makedirs(sparse_dir, exist_ok=True)

    run_colmap('feature_extractor', ['--database_path', db_path, '--image_path', image_dir, '--SiftExtraction.max_image_size', '2048'])
    run_colmap('exhaustive_matcher', ['--database_path', db_path])
    run_colmap('mapper', ['--database_path', db_path, '--image_path', image_dir, '--output_path', sparse_dir])

def run_dense(image_dir, sparse_dir, dense_dir):
    os.makedirs(dense_dir, exist_ok=True)
    run_colmap('image_undistorter', ['--image_path', image_dir, '--input_path', sparse_dir, '--output_path', dense_dir, '--output_type', 'COLMAP'])
    run_colmap('patch_match_stereo', ['--workspace_path', dense_dir, '--workspace_format', 'COLMAP', '--PatchMatchStereo.geom_consistency', 'true', '--PatchMatchStereo.max_image_size', '2048', '--PatchMatchStereo.num_samples', ])
    run_colmap('stereo_fusion', ['--workspace_path', dense_dir, '--workspace_format', 'COLMAP', '--StereoFusion.max_image_size', '2048', '--output_path', os.path.join(dense_dir, 'fused.ply')])
    
def run_geo_registration(sparse_dir, output_sparse_georef, db_path, align_type='enu', max_error=3.0):
    os.makedirs(output_sparse_georef, exist_ok=True)
    run_colmap('model_aligner', ['--input_path', sparse_dir, '--output_path', output_sparse_georef, '--database_path', db_path, '--ref_is_gps', '1', '--alignment_type', align_type, '--robust_alignment_max_error', str(max_error)])
