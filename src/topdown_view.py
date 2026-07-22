from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from plyfile import PlyData

# 저장소 구조(data/raw/)에 맞춘 경로. 파일명만 바꿔 쓰면 된다.
REPO_ROOT = Path(__file__).resolve().parents[1]
ply_path = REPO_ROOT / "data" / "raw" / "high.ply"

v = PlyData.read(str(ply_path))["vertex"]
pts = np.stack([v["x"], v["y"], v["z"]], axis=1)

print("num points:", pts.shape[0])
print("columns:", v.data.dtype.names)

# 너무 먼 점 제거
med = np.median(pts, axis=0)
keep = np.linalg.norm(pts - med, axis=1) < 5.0
pts = pts[keep]

# SH DC 색상 복원
C0 = 0.28209479177387814
if all(name in v.data.dtype.names for name in ["f_dc_0", "f_dc_1", "f_dc_2"]):
    dc = np.stack([v["f_dc_0"], v["f_dc_1"], v["f_dc_2"]], axis=1)[keep]
    rgb = np.clip(0.5 + C0 * dc, 0, 1)
else:
    print("f_dc 색상 필드가 없습니다. 회색으로 표시합니다.")
    rgb = np.ones_like(pts) * 0.5

# Y축이 up-axis라고 가정하고 지면 근처만 보기
y0 = np.median(pts[:, 1])
near = np.abs(pts[:, 1] - y0) < 0.3

print("near-ground points:", np.sum(near))

fig, ax = plt.subplots(figsize=(10, 10))
ax.scatter(pts[near, 0], pts[near, 2], c=rgb[near], s=0.5)

ax.set_aspect("equal")
ax.grid(True, alpha=0.3)
ax.set_xlabel("X (m)")
ax.set_ylabel("Z (m)")
ax.set_title("Top-down view: near-ground Gaussians")

plt.show()

plt.figure(figsize=(8, 5))
plt.hist(
    pts[:, 1] - np.median(pts[:, 1]),
    bins=300,
    range=(-5, 2),
    log=True
)
plt.xlabel("Y - median(Y) [m]")
plt.ylabel("count, log scale")
plt.axvline(0, color="k")
plt.title("Global vertical distribution")
plt.grid(True, alpha=0.3)
plt.show()

# =========================
# 캔 후보 찾기: 지면보다 5cm 이상 높은 점
# =========================
y0 = np.median(pts[:, 1])
hi_can = (pts[:, 1] - y0 > 0.05) & (pts[:, 1] - y0 < 0.25)

fig, ax = plt.subplots(figsize=(9, 9))
ax.scatter(pts[:, 0], pts[:, 2], c="lightgray", s=0.2)
ax.scatter(pts[hi_can, 0], pts[hi_can, 2], c=rgb[hi_can], s=3)

ax.set_aspect("equal")
ax.grid(True, alpha=0.3)
ax.set_xlabel("X (m)")
ax.set_ylabel("Z (m)")
ax.set_title("Can candidate: 5cm < height < 25cm")

print("캔 중심을 클릭하세요.")
p = plt.ginput(1, timeout=-1)
plt.show()

xc, zc = p[0]
print(f"can center: xc={xc:.3f}, zc={zc:.3f}")