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
