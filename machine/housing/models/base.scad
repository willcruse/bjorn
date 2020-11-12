/*
    Base module of Bjorn v3
    Units in mm
*/

$fn = 500;

// Main base dimensions
num_bottles = 6;
space_per_module = 150; // 15cm per bottle
width = num_bottles * space_per_module;
depth = 200;
height = 100;

// Rod Dimensions
rod_radius = 5;

platform_diameter = 100;
platform_thickness = 10;

module BaseBox(wall_thickness) {
   difference() {
       cube([width, depth, height]);
       translate([wall_thickness, wall_thickness, wall_thickness]) cube([width-(2*wall_thickness), depth-(2*wall_thickness), height]);
    }
}

module rail() {
    rotate([0, 90, 0]) cylinder(width, rod_radius, rod_radius, center=true);
}

module rail_attatchment() {
    size = platform_diameter/4;
    difference() {
       cube(size, center=true);
        rotate([0, 90, 0]) cylinder(size*2, rod_radius, rod_radius, center=true);
    }
}
module platform() {
    centre_box = depth/2;
    quarter_platform = platform_diameter/4;
    z_offset = height-rod_radius;
    union() {
        cylinder(platform_thickness, d=platform_diameter, center=true); //plate
        translate([0, quarter_platform*0.8, -quarter_platform/2]) rail_attatchment();
        translate([0, -quarter_platform*0.8, -quarter_platform/2])rail_attatchment();
    }
}
module rail_system() {
    centre_box = depth/2;
    half_platform = platform_diameter/4 * 0.8;
    z_offset = height-rod_radius;
    union() {
        translate([platform_diameter, centre_box, z_offset+platform_thickness]) platform();
        //Rails
        translate([0, centre_box+half_platform, z_offset-rod_radius/2]) rail();
        translate([0, centre_box-half_platform, z_offset-rod_radius/2]) rail();
    }
    
}

union() {
    BaseBox(10);
    translate([width/2, 0, 0]) rail_system();
}