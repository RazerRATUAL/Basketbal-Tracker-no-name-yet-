class ShotClassifier:
    def __init__(self, rim_bbox):
        """
        rim_bbox: (x1, y1, x2, y2) representing the rim bounding zone
        """
        self.rx1, self.ry1, self.rx2, self.ry2 = rim_bbox
        self.rim_center_x = (self.rx1 + self.rx2) / 2.0
        self.rim_center_y = (self.ry1 + self.ry2) / 2.0
        self.rim_radius = (self.rx2 - self.rx1) / 2.0
        
        self.trajectory = []
        self.above_rim_entry = False
        self.passed_cylinder = False
        self.state = "TRACKING"

    def update(self, ball_center):
        bx, by = ball_center
        self.trajectory.append(ball_center)

        # 1. Trajectory enters above the rim boundary
        if self.rx1 <= bx <= self.rx2 and by < self.ry1:
            self.above_rim_entry = True

        # 2. Trajectory passes through the cylinder zone from above
        if self.above_rim_entry and self.ry1 <= by <= self.ry2:
            if abs(bx - self.rim_center_x) < (self.rim_radius * 0.9):
                self.passed_cylinder = True

        # 3. Ball exits downward through the net
        if self.passed_cylinder and by > self.ry2 + 20:
            self.state = "MAKE"
            return self.state

        # 4. Ball drops below rim plane without clearing cylinder
        if by > self.ry2 + 50 and not self.passed_cylinder:
            self.state = "MISS"
            return self.state

        return self.state

if __name__ == "__main__":
    test_rim = (300, 200, 360, 230)
    classifier = ShotClassifier(test_rim)

    # Simulated descending swish
    simulated_arc = [
        (330, 160),
        (330, 190),
        (330, 215),
        (330, 260)
    ]

    print("--- Shot Classifier Check ---")
    for pt in simulated_arc:
        status = classifier.update(pt)
        print(f"Ball at {pt} -> State: {status}")
