from PySide2.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QCheckBox
import maya.cmds as cmds

class FrameRangeDialog(QDialog):
    def __init__(self):
        super(FrameRangeDialog, self).__init__()
        self.setWindowTitle("TurntableGen")
        self.setFixedSize(250, 320)  # Increased size to accommodate the checkbox and Execute button

        self.selected_object = None  # Store selected object temporarily

        self.initUI()

    def initUI(self):
        # Dropdown for selecting option
        self.option_label = QLabel("Select Option:")
        self.option_combobox = QComboBox()
        self.option_combobox.addItems(["Select Option", "Turntable", "Animation", "Other"])
        self.option_combobox.currentIndexChanged.connect(self.option_changed)

        # Widgets for frame range
        self.start_frame_label = QLabel("Start Frame:")
        self.start_frame_input = QLineEdit(str(int(cmds.playbackOptions(query=True, minTime=True))))
        self.start_frame_label.setVisible(False)
        self.start_frame_input.setVisible(False)

        self.end_frame_label = QLabel("End Frame:")
        self.end_frame_input = QLineEdit(str(int(cmds.playbackOptions(query=True, maxTime=True))))
        self.end_frame_label.setVisible(False)
        self.end_frame_input.setVisible(False)

        # Widgets for circle radius/distance
        self.radius_label = QLabel("Radius/Distance:")
        self.radius_input = QLineEdit("1.0")  # Default value
        self.radius_label.setVisible(False)
        self.radius_input.setVisible(False)

        # Widgets for circle height
        self.height_label = QLabel("Height:")
        self.height_input = QLineEdit("0.0")  # Default value
        self.height_label.setVisible(False)
        self.height_input.setVisible(False)

        # Checkbox for turntable around selected object
        self.checkbox_label = QLabel("Create turntable around selected object:")
        self.checkbox = QCheckBox()
        self.checkbox_label.setVisible(False)  # Default is unchecked
        self.checkbox.setVisible(False)  # Initially invisible

        # Checkbox for adding grid
        self.grid_checkbox_label = QLabel("Add Grid:")
        self.grid_checkbox = QCheckBox()
        self.grid_checkbox_label.setVisible(False)  # Default is unchecked
        self.grid_checkbox.setVisible(False)  # Initially invisible

        # Reminder note for turntable
        self.turntable_reminder_label = QLabel("Reminder: Make sure turntable object is selected.")
        self.turntable_reminder_label.setVisible(False)  # Initially invisible

        # Reminder note for animation
        self.animation_reminder_label = QLabel("Reminder: Make sure Camera or other object is selected.")
        self.animation_reminder_label.setVisible(False)  # Initially invisible

        # Animation parameters
        self.animation_linear_checkbox = QCheckBox("Make animation linear")
        self.animation_linear_checkbox.setVisible(False)
        self.animation_linear_checkbox.setChecked(False)

        self.animation_confirm_btn = QPushButton("Confirm")
        self.animation_confirm_btn.setVisible(False)

        # Preview button
        self.preview_btn = QPushButton("Preview")
        self.preview_btn.setVisible(False)

        # Execute button for "Other" option
        self.execute_btn = QPushButton("Execute")
        self.execute_btn.setVisible(False)
        self.execute_btn.clicked.connect(self.move_to_origin)

        # Description for "Other" option
        self.other_description_label = QLabel("/ note - MOVE OBJ TO WORLD CENTRE")
        self.other_description_label.setVisible(False)  # Initially invisible

        # Layout
        main_layout = QVBoxLayout()

        option_layout = QHBoxLayout()
        option_layout.addWidget(self.option_label)
        option_layout.addWidget(self.option_combobox)

        frame_range_layout = QVBoxLayout()
        frame_range_layout.addWidget(self.start_frame_label)
        frame_range_layout.addWidget(self.start_frame_input)
        frame_range_layout.addWidget(self.end_frame_label)
        frame_range_layout.addWidget(self.end_frame_input)

        radius_layout = QHBoxLayout()
        radius_layout.addWidget(self.radius_label)
        radius_layout.addWidget(self.radius_input)

        height_layout = QHBoxLayout()
        height_layout.addWidget(self.height_label)
        height_layout.addWidget(self.height_input)

        checkbox_layout = QHBoxLayout()
        checkbox_layout.addWidget(self.checkbox_label)
        checkbox_layout.addWidget(self.checkbox)

        grid_checkbox_layout = QHBoxLayout()
        grid_checkbox_layout.addWidget(self.grid_checkbox_label)
        grid_checkbox_layout.addWidget(self.grid_checkbox)

        main_layout.addLayout(option_layout)
        main_layout.addLayout(frame_range_layout)
        main_layout.addLayout(radius_layout)
        main_layout.addLayout(height_layout)
        main_layout.addLayout(checkbox_layout)  # Add checkbox
        main_layout.addLayout(grid_checkbox_layout)  # Add grid checkbox

        # Reminder notes layout
        reminder_layout = QVBoxLayout()
        reminder_layout.addWidget(self.turntable_reminder_label)
        reminder_layout.addWidget(self.animation_reminder_label)
        main_layout.addLayout(reminder_layout)

        # Animation layout
        animation_layout = QVBoxLayout()
        animation_layout.addWidget(self.animation_linear_checkbox)
        animation_layout.addWidget(self.animation_confirm_btn)
        main_layout.addLayout(animation_layout)

        # Preview and execute buttons layout
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.preview_btn)  # Add preview button
        btn_layout.addWidget(self.execute_btn)  # Add execute button
        self.ok_btn = QPushButton("OK")
        self.cancel_btn = QPushButton("Cancel")
        btn_layout.addWidget(self.ok_btn)
        btn_layout.addWidget(self.cancel_btn)

        main_layout.addLayout(btn_layout)

        # "Other" option layout
        other_option_layout = QVBoxLayout()
        other_option_layout.addWidget(self.other_description_label)
        main_layout.addLayout(other_option_layout)  # Add description to the main layout

        self.setLayout(main_layout)

        # Connect signals
        self.preview_btn.clicked.connect(self.preview)
        self.ok_btn.clicked.connect(self.create_motion_path_with_custom_frame_range_radius_and_height)
        self.cancel_btn.clicked.connect(self.reject)
        self.option_combobox.currentIndexChanged.connect(self.option_changed)
        self.animation_confirm_btn.clicked.connect(self.confirm_animation)

    def getFrameRange(self):
        start_frame = int(self.start_frame_input.text())
        end_frame = int(self.end_frame_input.text())
        return start_frame, end_frame

    def getRadius(self):
        return float(self.radius_input.text())

    def getHeight(self):
        return float(self.height_input.text())

    def createTurntableAroundSelectedObject(self):
        return self.checkbox.isChecked()

    def addGrid(self):
        return self.grid_checkbox.isChecked()

    def option_changed(self, index):
        if index == 1:  # "Turntable" option selected
            self.start_frame_label.setVisible(True)
            self.start_frame_input.setVisible(True)
            self.end_frame_label.setVisible(True)
            self.end_frame_input.setVisible(True)
            self.radius_label.setVisible(True)
            self.radius_input.setVisible(True)
            self.height_label.setVisible(True)
            self.height_input.setVisible(True)
            self.checkbox_label.setVisible(True)
            self.checkbox.setVisible(True)
            self.grid_checkbox_label.setVisible(True)
            self.grid_checkbox.setVisible(True)
            self.turntable_reminder_label.setVisible(True)  # Show reminder for turntable
            self.animation_reminder_label.setVisible(False)  # Hide animation reminder
            self.animation_linear_checkbox.setVisible(False)
            self.animation_confirm_btn.setVisible(False)
            self.preview_btn.setVisible(True)  # Show preview button
            self.execute_btn.setVisible(False)  # Hide execute button
            self.other_description_label.setVisible(False)  # Hide description for "Other" option
        elif index == 2:  # "Animation" option selected
            self.start_frame_label.setVisible(False)
            self.start_frame_input.setVisible(False)
            self.end_frame_label.setVisible(False)
            self.end_frame_input.setVisible(False)
            self.radius_label.setVisible(False)
            self.radius_input.setVisible(False)
            self.height_label.setVisible(False)
            self.height_input.setVisible(False)
            self.checkbox_label.setVisible(False)
            self.checkbox.setVisible(False)
            self.grid_checkbox_label.setVisible(False)
            self.grid_checkbox.setVisible(False)
            self.turntable_reminder_label.setVisible(False)  # Hide turntable reminder
            self.animation_reminder_label.setVisible(True)  # Show animation reminder
            self.animation_linear_checkbox.setVisible(True)
            self.animation_confirm_btn.setVisible(True)
            self.preview_btn.setVisible(False)  # Hide preview button
            self.execute_btn.setVisible(False)  # Hide execute button
            self.other_description_label.setVisible(False)  # Hide description for "Other" option
        elif index == 3:  # "Other" option selected
            self.start_frame_label.setVisible(False)
            self.start_frame_input.setVisible(False)
            self.end_frame_label.setVisible(False)
            self.end_frame_input.setVisible(False)
            self.radius_label.setVisible(False)
            self.radius_input.setVisible(False)
            self.height_label.setVisible(False)
            self.height_input.setVisible(False)
            self.checkbox_label.setVisible(False)
            self.checkbox.setVisible(False)
            self.grid_checkbox_label.setVisible(False)
            self.grid_checkbox.setVisible(False)
            self.turntable_reminder_label.setVisible(False)
            self.animation_reminder_label.setVisible(False)
            self.animation_linear_checkbox.setVisible(False)
            self.animation_confirm_btn.setVisible(False)
            self.preview_btn.setVisible(False)
            self.execute_btn.setVisible(True)  # Show execute button
            self.other_description_label.setVisible(True)  # Show description for "Other" option
        else:  # Any other option selected
            self.start_frame_label.setVisible(False)
            self.start_frame_input.setVisible(False)
            self.end_frame_label.setVisible(False)
            self.end_frame_input.setVisible(False)
            self.radius_label.setVisible(False)
            self.radius_input.setVisible(False)
            self.height_label.setVisible(False)
            self.height_input.setVisible(False)
            self.checkbox_label.setVisible(False)
            self.checkbox.setVisible(False)
            self.grid_checkbox_label.setVisible(False)
            self.grid_checkbox.setVisible(False)
            self.turntable_reminder_label.setVisible(False)
            self.animation_reminder_label.setVisible(False)
            self.animation_linear_checkbox.setVisible(False)
            self.animation_confirm_btn.setVisible(False)
            self.preview_btn.setVisible(False)
            self.execute_btn.setVisible(False)  # Hide execute button
            self.other_description_label.setVisible(False)  # Hide description for "Other" option

    def move_to_origin(self):
        selection = cmds.ls(selection=True)
        for obj in selection:
            cmds.xform(obj, translation=[0, 0, 0])

    def preview(self):
        # Delete previously created circle, if any
        if cmds.objExists("preview_circle"):
            cmds.delete("preview_circle")

        radius = self.getRadius()
        height = self.getHeight()
        create_around_selected_object = self.createTurntableAroundSelectedObject()

        if create_around_selected_object:
            # Get selected object(s)
            selection = cmds.ls(selection=True)
            if not selection:
                cmds.warning("Please select an object.")
                return
            self.selected_object = selection[0]  # Store selected object
            selected_object = selection[0]

            # Get translation of the selected object
            translate_values = cmds.xform(selected_object, query=True, translation=True, worldSpace=True)
            translate_x, translate_y, translate_z = translate_values

            # Create circle
            circle = cmds.circle(center=[translate_x, translate_y, translate_z], normal=[0, 1, 0], radius=radius, sections=8, degree=3)[0]

            # Move the circle
            cmds.move(-0.153587, height, 0, circle, absolute=True)
        else:
            # Create circle at the center
            circle = cmds.circle(center=[0, 0, 0], normal=[0, 1, 0], radius=radius, sections=8, degree=3)[0]

            # Move the circle
            cmds.move(-0.153587, height, 0, circle, absolute=True)

        # Rename the circle for easy identification
        cmds.rename(circle, "preview_circle")

        # Refresh the viewport to display the created circle
        cmds.refresh()

    def create_motion_path_with_custom_frame_range_radius_and_height(self):
        # Show frame range, radius, and height dialog
        if self.option_combobox.currentIndex() == 1:  # "Turntable" option selected
            start_frame, end_frame = self.getFrameRange()
            radius = self.getRadius()
            height = self.getHeight()
            create_around_selected_object = self.createTurntableAroundSelectedObject()
            add_grid = self.addGrid()

            if add_grid:
                # Create a 100x100 grid
                cmds.polyPlane(width=500, height=500, subdivisionsWidth=500, subdivisionsHeight=100, name="grid")

            # If checkbox is checked and an object is selected, create turntable around the selected object
            if create_around_selected_object:
                # Get translation of the selected object
                translate_values = cmds.xform(self.selected_object, query=True, translation=True, worldSpace=True)
                translate_x, translate_y, translate_z = translate_values

                # Create circle
                circle = cmds.circle(center=[translate_x, translate_y, translate_z], normal=[0, 1, 0], radius=radius, sections=8, degree=3)[0]

                # Move the circle
                cmds.move(-0.153587, height, 0, circle, absolute=True)
            else:
                # Create circle at the center
                circle = cmds.circle(center=[0, 0, 0], normal=[0, 1, 0], radius=radius, sections=8, degree=3)[0]

                # Move the circle
                cmds.move(-0.153587, height, 0, circle, absolute=True)

            # Create camera with automatic name 'Turntable Camera'
            camera = cmds.camera(name='Turntable_Camera')[0]

            # Clear selection and select camera and circle
            cmds.select(clear=True)
            cmds.select(camera, circle)

            # Create motion path with custom frame range
            motion_path = cmds.pathAnimation(fractionMode=True, follow=True, followAxis="x", upAxis="y", worldUpType="vector", worldUpVector=[0, 1, 0], inverseUp=False, inverseFront=False, bank=False, startTimeU=start_frame, endTimeU=end_frame)[0]
            cmds.cutKey(motion_path, time=(start_frame, end_frame), attribute='uValue')
        elif self.option_combobox.currentIndex() == 2:  # "Animation" option selected
            pass  # No action needed here, as animation will be confirmed by the user
        self.accept()

    def confirm_animation(self):
        if self.animation_linear_checkbox.isChecked():
            # Get the name of the currently selected object
            selected_objects = cmds.ls(selection=True)
            if not selected_objects:
                cmds.warning("Please select an object.")
                return
            selected_object = selected_objects[0]  # Assuming only one object is selected

            # Find the motion path node associated with the selected object
            motion_path_nodes = cmds.listConnections(selected_object, type="motionPath")
            if not motion_path_nodes:
                cmds.warning("Selected object is not attached to a motion path.")
                return
            motion_path_node = motion_path_nodes[0]  # Assuming only one motion path node is found

            # Get the name of the motion path node
            motion_path_name = motion_path_node.split("|")[-1]

            # Get the timeline range
            start_frame = cmds.playbackOptions(query=True, minTime=True)
            end_frame = cmds.playbackOptions(query=True, maxTime=True)

            # Select the currently selected object
            cmds.select(selected_object, r=True)

            # Clear selection of keyframes
            cmds.selectKey(cl=True)

            # Add keyframes for motion path uValue from start_frame to end_frame
            cmds.selectKey(motion_path_name + ".uValue", add=True, k=True, t=(start_frame, end_frame))

            # Set keyframe tangents to linear
            cmds.keyTangent(itt="linear", ott="linear")
        else:
            cmds.warning("Please check the 'Make animation linear' checkbox before confirming.")

# Launch the UI
app = QApplication.instance()
if not app:
    app = QApplication([])
dialog = FrameRangeDialog()
dialog.show()
app.exec_()
