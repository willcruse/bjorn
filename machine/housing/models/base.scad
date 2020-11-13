/*
    Base module of Bjorn v3
    Units in mm
*/

$fn = 500;

// Main base dimensions
num_bottles = 6;
//space_per_module = 150; // 15cm per bottle
//width = num_bottles * space_per_module;

width = 1000;
space_per_module = 1000/num_bottles;
echo("Space per bottle: ", space_per_module);

depth = 100;
height = 100;

// Rod Dimensions
rod_radius = 5;

platform_diameter = 80;
platform_thickness = 10;

module base_box(wall_thickness) {
   difference() {
       cube([width+(2*wall_thickness), depth+(2*wall_thickness), height]);
       translate([wall_thickness, wall_thickness, wall_thickness]) cube([width, depth, height]);
    }
}
module rail() {
    rotate([0, 90, 0]) cylinder(width, rod_radius, rod_radius, center=true);
}

module linear_bearing(solid=false) {
    difference() {
        cylinder(platform_diameter+2, 19/2, 19/2, center=true);
        if (!solid) {
            translate([0, 0, -1]) cylinder(platform_diameter+2, 10/2, 10/2, center=true);
        }
    }
}

module rail_attatchment() {
    difference() {
        cube([platform_diameter, 25, 25], center=true);
        translate([0, 0, -1]) rotate([0, 90, 0]) linear_bearing(solid=true);
    }
}
module platform() {
    centre_box = depth/2;
    third_platform = platform_diameter/3;
    z_offset = height-rod_radius;
    union() {
        cylinder(platform_thickness, d=platform_diameter, center=true); //plate
        translate([0, third_platform*0.8, -third_platform/2]) rail_attatchment();
        translate([0, -third_platform*0.8, -third_platform/2])rail_attatchment();
    }
}
module rail_system() {
    centre_box = depth/2;
    third_platform = platform_diameter/4;
    z_offset = height-rod_radius;
    union() {
        translate([platform_diameter, centre_box, z_offset+platform_thickness]) platform();
        //Rails
        translate([0, centre_box+third_platform, z_offset-rod_radius]) rail();
        translate([0, centre_box-third_platform, z_offset-rod_radius]) rail();
    }
    
}
module back_box(wall_thickness) {
    back_height = 300+height;
    cube([width+2*wall_thickness, 20, back_height]);
}


union() {
    wall_thickness = 10;
    base_box(wall_thickness);
    translate([0, depth+2*wall_thickness, 0]) back_box(wall_thickness);
    translate([width/2, 0, 0]) rail_system();
}