float search_dist = 3.0;
vector hit_point;
float hu, hv;

int hit_prim = intersect(1, @P, -@N * search_dist, hit_point, hu, hv);

if(hit_prim != -1) {
	vector hit_norm = prim_normal(1, hit_prim, hu, hv);

	if (dot(@N, hit_norm) < 0) {
		f@deform_dist = length(@P - hit_point);
		@P = hit_point;
	}
}

# ------------

if(f@deform_dist == 0) {
	int handle = pcopen(0, "P", @P, 10000, 50);

	float n_deform_dist;
	float sum = 0;

	while(pciterate(handle)) {
		pcimport(handle, "deform_dist", n_deform_dist);
		sum += n_deform_dist;
	}

	f@bulge_factor = sum;
}

#-----------

float bulge_scale = ch("bulge_scale");
if (f@deform_dist == 0) {
	@P += @N * f@bulge_factor * bulge_scale;
}
