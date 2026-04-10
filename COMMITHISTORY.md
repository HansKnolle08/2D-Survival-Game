# 2D Survival Game

## Commit History:

HansKnolle08 (9. April 2026 um 12:49)

Initial commit

- Added World creation
- Added Player (+Movement)
- Base Project Structure

11 files changed, 120 insertions(+)

4a8a591717e49544f16380463fdee3af1b4664be

---

HansKnolle08 (9. April 2026 um 13:04)

Commit 09.04.2026 13:05

- FPS doesn't influence Player Speed anymore

2 files changed, 8 insertions(+), 7 deletions(-)

c1538ecab5f95b0ad50bba6967670d7d9427cc0c

--- 

HansKnolle08 (9. April 2026 um 13:18)

Commit 09.04.2026 13:18

- Moved rendering to a seperate file

3 files changed, 35 insertions(+), 27 deletions(-)

78b436787dbc1ac46b53298eafa812a05c9bc021

---

HansKnolle08 (9. April 2026 um 16:14)

Commit 09.04.2026 16:13

- Refactored a lot of code to make it look better
- Added more comments for my understanding
- Added Type Annotations
- Created new file update.py which contains the update() function that now handles the updating of the game
- update() also returns the camera_x and camera_y used by the renderer and also it returns delta which may be useful in the future

6 files changed, 66 insertions(+), 18 deletions(-)

df30c1ef268feb799e7cf0e033071fe847c9d324

---

HansKnolle08 (9. April 2026 um 16:24)

Commit 09.04.26 16:23

- Added License
- Added Readme

2 files changed, 76 insertions(+)

9c650135d24a3b331b6da3bfc19f092475afd386

---

HansKnolle08 (9. April 2026 um 21:56)

Commit 09.04.2026 21:56

-Added Health and Food System
-Added food which randomly generates in the world. Restores Hunger
-Added an Inventory System (Base Structure)

7 files changed, 224 insertions(+), 5 deletions(-)

5beb3767193ea5fb01be174a715e6219af3564a8

---

HansKnolle08 (9. April 2026 um 21:58)

Edited Readme

1 file changed, 15 insertions(+), 1 deletion(-)

814f949e37dd9980a78567715a3e3c9b8733d9f7

---

HansKnolle08 (10. April 2026 um 07:25)

Commit 10.04.2026 7:25

- Removed Food System
- Added Mouse Interactions to both World and Inventory

5 files changed, 114 insertions(+), 88 deletions(-)

ff5377532b837ca6dcff49fef971268cc4d2d7a0

---

HansKnolle08 (10. April 2026 um 12:56)

Commit 10.04.2626 12:56

- Added first world Object: Trees
- Added Breaking and resource gaining mechanic
- Tweaked Player Generation and UI looks and feels a bit
- Moved gameplay relevant Variables and Constants to gameplay_config.py

9 files changed, 471 insertions(+), 54 deletions(-)

ac79b94de44ef71a83ec40c80b448ab271bb3fb1

---

HansKnolle08 (10. April 2026 um 12:58)

Commit 10.04.2026 12:58

- Small refactoring in gameplay_config.py

2 files changed, 20 insertions(+), 4 deletions(-)

1dd3c91daf56bc5c5dfe69e0b98c9ab1f26f4ba9

---

HansKnolle08 (10. April 2026 um 14:04) 

Commit 10.05.2026 14:03 (Little typo in commit message, its the 10.04.26)

- Added Entity Structure with an Entity and Mob class, a mob manager and the first mob a sheep which extends the mob class
- Added hitting mechanic and mob loot dropping

12 files changed, 389 insertions(+), 17 deletions(-)

1bafa1462ce1ffc8f157f9cca640502d1c046432

---

HansKnolle08 (10. April 2026 um 14:06)

Edited Readme

1 file changed, 13 insertions(+)

23346e620833903633d8fa0eb339d628fe338799

---