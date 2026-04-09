# 2D Survival Game

## Commit History: (Commit History intendendly excludes Readme updates)

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