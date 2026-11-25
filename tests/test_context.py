"""验证业务输入之间的引用关系及形状，不计算目标输出。"""
import numpy as np
from support.inspect_data import load_bundle

def test_linked_materials():
    _, arrays, r, scenarios = load_bundle()
    calibration={v['batch_id'] for v in r['collections'] if v['role']=='calibration'}
    holdout={v['batch_id'] for v in r['collections'] if v['role']=='holdout'}
    assert calibration and holdout and not calibration&holdout
    assert arrays['weight'].shape[1]*r['convolution']['groups'] == arrays['integer_input'].shape[1]
    assert all(v['tensor'] in arrays for v in r['collections'])
