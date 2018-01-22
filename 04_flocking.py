//Test
float min_dist = ch("min_dist");
float max_dist = ch("max_dist");
float exponent = ch("exponent");
int complimemnt = chi("compliment");

vector lookup_pt = {0, 0, 0};
vector lookup_vec = lookup_pt - @P;
float distance = length(lookup_vec);
vector lookup_dir = normalize(lookup_vec);

float range = max_dist - min_dist;
float norm_dist = (clamp(distance, min_dist, max_dist) - min_dist) / range;
float result = pow(norm_dist, exponent);

if(complimemnt) {
    result = 1 - result;
}

@Cd.r = result;
@Cd.g = 0;
@Cd.b = 0;

--------------
//boid_sim
//initial_state
v@v = {0, 0, 5};
v@v.z += fit01(rand(@ptnum), {-5, -5, -5}, {5, 5, 5});
v@accel = {0, 0, 0};
v@N = normalize(v@v);
v@up = {0, 1, 0};

v@P = fit01(rand(@ptnum), {-5, -5, -5}, {5, 5, 5});

f@mass = 1;
i@id = @ptnum;
-------------
//update
@v += @accel * @TimeInc;

@P += @v * @TimeInc;

@accel = {0, 0, 0};
---------------
//cohesion
float min_dist = ch("min_dist");
float max_dist = ch("max_dist");
float max_strength = ch("max_strength");

vector flock_center = detail(0, "flock_center", 0);

vector lookup_vec = flock_center - @P;

float distance = length(lookup_vec);
vector lookup_dir = normalize(lookup_vec);

float range = max_dist - min_dist;
float norm_dist = (clamp(distance, min_dist, max_dist) - min_dist) / range;

v@accel += lookup_dir * norm_dist * max_strength;

-----------------
//aligment
float max_radius = 99999;
int max_neighbors = 7;
int handle = pcopen(0, "P", @P, max_radius, max_neighbors + 1);

int near_pt;
int near_count = 0;
vector near_v;
vector accum_v = {0, 0, 0};

while(pciterate(handle)) {
    pcimport(handle, "point.number", near_pt);
    if(near_pt == @ptnum) {
        continue;
    }
    pcimport(handle, "v", near_v);
    accum_v += near_v;
    near_count++;
}

if(near_count != 0) {
    accum_v /= (float)near_count;
    v@accel += (accum_v - @v) * 0.5;
}
------------------
//falloff_strength_with_scale_factor
float min_dist      = ch("min_dist");
float max_dist      = ch("max_dist");
float max_strength  = ch("max_strength");
int   max_neighbors = 10;
float max_radius    = 999999;

int    near_ptnum;
float  distance, strength, norm_dist;
vector near_p, to_near_vec, to_near_dir;

vector accum = {0,0,0};
float  range = max_dist - min_dist;

int handle = pcopen(0, "P", @P, max_radius, max_neighbors + 1);

while(pciterate(handle)) {
    pcimport(handle, "point.number", near_ptnum);
    if (near_ptnum == @ptnum)
        continue; // skip ourselves, we're in the point cloud!

    // find the neighboring point's position
    pcimport(handle, "P", near_p);

    // find the vector from us to the neighbor
    to_near_vec = near_p - @P;

    // how far is that?
    distance = length(to_near_vec);

    // and lets remember the direction, just a unit length vector pointing
    // to our neighbor that we can scale later
    to_near_dir = normalize(to_near_vec);

    // clamp and normalize distance in the 0 - 1 range
    norm_dist = (clamp(distance, min_dist, max_dist) - min_dist) / range;

    // now that we're 0 - 1, we can lookup into the falloff ramp
    strength = chramp("falloff_ramp", norm_dist) * max_strength;

    // lets accumulate an acceleration away from this point
    accum += (-to_near_dir) * strength;
}

// add to existing acceleration for this time step
v@accel += accum;
