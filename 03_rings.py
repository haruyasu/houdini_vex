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
}

segment(0.75, 1.25, 0, 0.5, 10);
