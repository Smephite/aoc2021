import sys, os

from numpy.matrixlib import mat
sys.path.append(os.path.abspath("."))
import aoc
import numpy as np

probes = {}

for probe_info in aoc.raw_aoc().split("\n\n"):
    lines = probe_info.split("\n")
    name = lines[0].replace("-", "").replace(" ", "").replace("scanner", "")
    beacons = []
    for beacon in lines[1:]:
        if beacon == "":
            continue
        (x, y, z) = beacon.split(",")
        beacons.append((int(x),int(y),int(z)))
    probes[int(name)] = beacons


sin = {0: 0, 1: 1, 2: 0, 3: -1}
cos = {0: 1, 1: 0, 2: -1, 3: 0}

def rotation_matrix(yaw, pitch, roll):
    yaw = yaw % 4      # yaw   around z (up)
    pitch = pitch % 4  # pitch around y (side)
    roll = roll % 4    # roll  around x (forward)

    return np.array([[cos[yaw]*cos[pitch], cos[yaw]*sin[pitch]*sin[roll]-sin[yaw]*cos[roll], cos[yaw]*sin[pitch]*cos[roll]+sin[yaw]*sin[roll]],
                    [sin[yaw]*cos[pitch], sin[yaw]*cos[pitch]*sin[roll]+cos[yaw]*cos[roll], sin[yaw]*sin[pitch]*cos[roll]-cos[yaw]*sin[roll]],
                    [-sin[pitch], cos[pitch]*sin[roll], cos[pitch]*cos[roll]]])

def rotate_fast(positions, int):
    return [rotate_fast_single(p, int) for p in positions]

def rotate_fast_single(position, int):
    (x, y, z) = position
    if int == 0:
        return ( x,  y,  z)
    if int == 1 :
         return ( x,  z, -y)
    if int == 2 :
         return ( x, -y, -z)
    if int == 3 :
         return ( x, -z,  y)
    if int == 4 :
         return ( y,  x, -z)
    if int == 5 :
         return ( y,  z,  x)
    if int == 6 :
         return ( y, -x,  z)
    if int == 7 :
         return ( y, -z, -x)
    if int == 8 :
         return ( z,  x,  y)
    if int == 9 :
         return ( z,  y, -x)
    if int == 10:
         return ( z, -x, -y)
    if int == 11:
         return ( z, -y,  x)
    if int == 12:
         return (-x,  y, -z)
    if int == 13:
         return (-x,  z,  y)
    if int == 14:
         return (-x, -y,  z)
    if int == 15:
         return (-x, -z, -y)
    if int == 16:
         return (-y,  x,  z)
    if int == 17:
         return (-y,  z, -x)
    if int == 18:
         return (-y, -x, -z)
    if int == 19:
         return (-y, -z,  x)
    if int == 20:
         return (-z,  x, -y)
    if int == 21:
         return (-z,  y,  x)
    if int == 22:
         return (-z, -x,  y)
    if int == 23:
         return (-z, -y, -x)

def rotate_probe(positions, yaw, pitch, roll):
    rot_matrix = rotation_matrix(yaw, pitch, roll)
    new_pos = []
    for pos in positions:
        pp = np.transpose(np.matmul(rot_matrix,np.transpose([pos])))[0]
        new_pos.append((pp[0], pp[1], pp[2]))
    return new_pos

def translate_positions(positions, translation, neg = False):
    pre = -1 if neg else 1
    return [(p[0] + pre*translation[0], p[1] + pre*translation[1], p[2] + pre*translation[2]) for p in positions]



defined_beacons = []

probe_positions = {0: ((0, 0, 0), (0, 0, 0))}

#probe_positions = {0: ((0, 0, 0), (0, 0, 0)),
# 14: ((114  , -1031, 35   ), (0, 2, 0)),
# 15: ((131  , -1099, 1290 ), (3, 3, 0)),
# 7 : ((179  , -2321, 1186 ), (0, 2, 1)),
# 20: ((86   , -3584, 1219 ), (0, 3, 0)),
# 4 : ((55   , -3610, 2500 ), (1, 1, 0)),
# 25: ((187  , -3568, 3556 ), (0, 1, 0)),
# 10: ((1387 , -3564, 1219 ), (2, 1, 0)),
# 19: ((-1093, -3601, 2390 ), (2, 2, 0)),
# 1 : ((1322 , -2282, 1116 ), (3, 0, 0)),
# 2 : ((2403 , -2246, 1125 ), (1, 0, 0)),
# 8 : ((3669 , -2272, 1278 ), (2, 3, 0)),
# 9 : ((3625 , -3552, 1237 ), (2, 0, 0)),
# 13: ((132  , -3536, 27   ), (2, 0, 1)),
# 18: ((-1128, -2352, -53  ), (3, 1, 0)),
# 24: ((12   , -4701, 31   ), (3, 2, 0)),
# 17: ((100  , -6004, 0    ), (0, 1, 0)),
# 12: ((146  , -7152, -60  ), (3, 2, 0)),
# 3 : ((-1028, -7104, -25  ), (1, 3, 0)),
# 11: ((1347 , -7167, -19  ), 8),
# 16: ((14   , -2321, 21   ), 22),
# 21: ((1323 , -5838, -15  ), 10),
# 26: ((122  , -1220, -1233), 20),
# 6 : ((-1083, -1099, -1143), 3),
# 22: ((1193 , -1223, -1188), 1),
# 5 : ((2412 , -1193, -1206), 20),
# 23: ((1279, 55, -1180), 18)}

unknown_beacons = dict(probes)


for known_probe in probe_positions.keys():
    rotation = probe_positions[known_probe][1]
    rel_pos = unknown_beacons.pop(known_probe)
    if isinstance(rotation, int):
        rel_pos = rotate_fast(rel_pos, rotation)
        pass
    else:
        rel_pos = rotate_probe(rel_pos, rotation[0], rotation[1], rotation[2])
    defined_beacons += translate_positions(rel_pos, probe_positions[known_probe][0])

defined_beacons = list(set(defined_beacons))


def find_match(rel_positions, required_match = 12):
    known_probe_pos = None
    for rel_beacon in rel_positions:
        if known_probe_pos != None:
            break
        # we will try to move rel_probe to each known probe position and check if other probes are matching

        centered_beacon = translate_positions(rel_positions, rel_beacon, True)
        for known_beacon in defined_beacons:
            matched_beacon = translate_positions(centered_beacon, known_beacon)
            matched_count = len(list(filter(lambda b : b in defined_beacons, matched_beacon)))
            if matched_count >= required_match:
                known_probe_pos = (known_beacon[0] - rel_beacon[0], known_beacon[1] - rel_beacon[1], known_beacon[2] - rel_beacon[2])
                break
    return known_probe_pos

REQUIRED_MATCHES = 12

while len(unknown_beacons.values()) != 0:
    match = False
    for probe in list(unknown_beacons.keys()):
        if match:
            match = False
            break
        for i in range(0, 24):
            probe_senses = rotate_fast(unknown_beacons[probe], i)
            matched_pos = find_match(probe_senses, REQUIRED_MATCHES)
            if matched_pos is not None:
                print(f"Probe {probe} @ {matched_pos} / {i}")
                probe_positions[probe] = (matched_pos, i)
                match = True
                initial_frame_beacons = translate_positions(rotate_fast(unknown_beacons.pop(probe), i), matched_pos)
                defined_beacons += initial_frame_beacons
                break
                    

max_dist = 0
for p1 in probe_positions.values():
    p1 = p1[0]
    for p2 in probe_positions.values():
        p2 = p2[0]
        max_dist = max(max_dist, abs(p1[0]-p2[0])+abs(p1[1]-p2[1])+abs(p1[2]-p2[2]))

print(f"The max distance between two scanners is {max_dist}.")