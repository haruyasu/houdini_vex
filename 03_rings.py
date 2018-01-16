#define TAU 6.283185307179586
#define PI  3.141592653589793

int segment(float rad_min; float rad_max; float start_theta; float end_theta; int resolution;) {
    float theta;
    int pt;
    int prim = addprim(geoself(), "poly");
    float theta_step = (end_theta - start_theta) / (float)resolution;

    // inner radius
    for(int step = 0; step < resolution+1; step++) {
        theta = start_theta + (theta_step * step);
        pt = addpoint(geoself(), set(cos(theta) * rad_min, sin(theta) * rad_min, 0));
        addvertex(geoself(), prim, pt);
    }

    // outer radius
    for(int step = 0; step < resolution+1; step++) {
        theta = end_theta - (theta_step * step);
        pt = addpoint(geoself(), set(cos(theta) * rad_max, sin(theta) * rad_max, 0));
        addvertex(geoself(), prim, pt);
    }
    return prim;
}

int ring(float min_arc;
         float max_arc;
         float radius_min;
         float radius_max;
         float skip_chance;
         int   ring_id;
         float ring_seed;) {

    float theta = 0;
    float rand_step;
    int seg_num = ring_id;

    // ring logic
    while(1) {
        rand_step = fit01(rand(seg_num * ring_seed), min_arc, max_arc);

        if(rand(seg_num + 9323 * ring_seed) > skip_chance) {
            segment(radius_min, radius_max, theta, theta + rand_step, 15);
        }
        theta += rand_step;
        seg_num++;

        if(theta >= TAU) {
            break;
        }
    }

    return 1;
}

//entire system
int num_rings = chi("num_rings");
float rings_start = 0.5;
float rings_end = 10.0;
float rings_step = (rings_end - rings_start) / (float)num_rings;
float rings_radius = rings_start;
float seed = ch("seed");

for(int i=0; i < num_rings; i++) {
    ring(0.01, 1.0, rings_radius, rings_radius * 1.2, 0.3333, i, seed);
    rings_radius += rings_step;
}

//ring(0.05, 0.5, 0.75, 1.0, 0.333);
