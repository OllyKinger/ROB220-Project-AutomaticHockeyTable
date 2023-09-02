# ROB220_OK_EM

## Description of project 
This project was created for the ROB220 assignment brief, The brieft that we decided to do was to make an artefact for the robotics stand at the expo. We chose that we were going to make a robot air hockey table that will play the user and potentially be impossible to beat. We designed a table that had a rail mounted on it which would move back and forth to block the puck from entering the goal, to track the puck it would use a camera mounted above the table. It would use machine vision to track the puck using opencv. 

## Installation/Setup instructions

### Software requirements 
To install the project you will need to clone the repository to your local machine. You will need to have python 3.7 installed on your machine. You will also need to install the following packages using pip:
- opencv-python
- numpy-python
- pygame-python
- Accel.Stepper - Arduino

You will need to update all of these packages to be compatible with whatever version of python and arduino that you are using.

## Why

This was created for the ROB220 module in the second year of my degree, the module focused on human robot interaction and we were tasked with creating an interactive expericence for an exhibition.

### Components
You will also need the the custom built hockey [table](https://www.amazon.co.uk/dp/B097DVCZ4X?psc=1&ref=ppx_yo2ov_dt_b_product_details), this is the table that we used for the project. You will also need to have an [arduino uno](https://www.amazon.co.uk/ELEGOO-Arduino-Arduino-Compatible-Transfer-Operation/dp/B09JWFTZ2V/ref=sr_1_1_sspa?adgrpid=55885013711&hvadid=606028184073&hvdev=c&hvlocphy=9045283&hvnetw=g&hvqmt=e&hvrand=13831305461097289309&hvtargid=kwd-296166484280&hydadcr=3759_2326425&keywords=arduino+uno&qid=1683646332&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1) and a stepper motor driver as well as a suitable stepper motor and linear rail system to move the rail. You will also need a camera to mount above the table to track the puck it does not matter which one you use as it has to be calibrated anyway but we used [this one](https://www.amazon.co.uk/gp/product/B08JYD85Y1/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1).

This section is only relevant if you are trying to recreate the project, otherwise just move onto the next section.

### wiring 

The wiring for the project is just between the arduino, the stepper motor and the motor driver. The following images show how the project should be wired: 


### Running the project 
In order to get the project working you will need to run the following files in the following order: 
1. Main Project.py
2. Main_Arduino_Code.ino
It is important to make sure that you run them in this order as otherwise it will cause problems with the serial bus.

It is also important to make sure that you have the correct COM port selected in the python file, this can be found by going to device manager and looking under the ports section. 
The rail also needs to be moved(by hand) all the way to the end of the rail(the end without the cogs on it) before running the project as otherwise it will not work properly.  


### Troubleshooting 

- One of the potential problems with the setup is the use of 3d printed parts in the rail system, these have the potential to break, the main components that may break are the cogs and the holder for the striker, if these break they can easily be 3d printed again due to the designs being included in the project.
- There are a lot of files included in the project that are not used in the final setup of the project, this is because they were used in prototyping and testing of the project, we left them in to allow for someone to follow through our process of creating the project if they wanted to.

## Why 

This project was created for the ROB220 module in the second year of my degree, the focus of the module was on human robot interaction and we were tasked with creating an experience for an exhibit.

I created this project in collaboration with Elijah Marbek.

The code In this repo is only the final product and a lot of iteration and testing went into getting to this point.

