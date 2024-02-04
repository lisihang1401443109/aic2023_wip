import os

WHERE_IS_CAM = {
  'test': {'S001': ['c001', 'c002', 'c003', 'c004', 'c005', 'c006', 'c007'],
    'S003': ['c014', 'c015', 'c016', 'c017', 'c018', 'c019'],
    'S009': ['c047', 'c048', 'c049', 'c050', 'c051', 'c052'],
    'S014': ['c076', 'c077', 'c078', 'c079', 'c080', 'c081'],
    'S018': ['c100', 'c101', 'c102', 'c103', 'c104', 'c105'],
    'S022': ['c124', 'c125', 'c126', 'c127', 'c128', 'c129'],
    'S021': ['c118', 'c119', 'c120', 'c121', 'c122', 'c123']
    },
  'train': {'S012': ['c065', 'c066', 'c067', 'c068', 'c069', 'c070'],
    'S011': ['c059', 'c060', 'c061', 'c062', 'c063', 'c064'],
    'S002': ['c008', 'c009', 'c010', 'c011', 'c012', 'c013'],
    'S004': ['c020', 'c021', 'c022', 'c023', 'c024'],
    'S006': ['c030', 'c031', 'c032', 'c033', 'c034', 'c035'],
    'S007': ['c036', 'c037', 'c038', 'c039', 'c040'],
    'S010': ['c053', 'c054', 'c056', 'c055', 'c057', 'c058'],
    'S015': ['c082', 'c083', 'c086', 'c084', 'c085', 'c087'],
    'S019': ['c107', 'c106', 'c108', 'c109', 'c110', 'c111'],
    'S016': ['c092', 'c090', 'c089', 'c091', 'c093', 'c088']
    },
  'validation': {'S005': ['c025', 'c026', 'c027', 'c028', 'c029'],
    'S008': ['c041', 'c042', 'c043', 'c044', 'c045', 'c046'],
    'S013': ['c071', 'c072', 'c073', 'c074', 'c075'],
    'S017': ['c094', 'c095', 'c096', 'c097', 'c098', 'c099'],
    'S020': ['c112', 'c113', 'c114', 'c115', 'c116', 'c117']
    }
  }

DATA_FOLDER_PATH = '/WAVE/workarea/users/sli13/AIC23_MTPC/data/aic23/'

def path_from_scenecam(scenecam : 'tuple[str, str]', ) -> str:
  
  if len(scenecam) != 2:
    scenecam = scenecam.split('/')
  
    scene = scenecam[0]
    cam = scenecam[1]
    
    usage = None
    for _usage in ['train', 'validation', 'test']:
        if scene in WHERE_IS_CAM[_usage]:
            usage = _usage
            break
    if usage is None:
        raise ValueError(f'Unknown scene {scene}')
    
    return os.path.join(DATA_FOLDER_PATH, usage, scene, cam)
  
  
'''
  look for which scene a specific camera belongs to
'''
def scene_from_cam(cam: str) -> str:
    for usage, scenes in WHERE_IS_CAM.items():
        for scene, cams in scenes.items():
            if cam in cams:
                return scene
  