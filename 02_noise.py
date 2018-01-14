float  freq    = ch("freq"); // 1.0 / scale of noise
vector offset  = chv("offset");
float  amp     = ch("amp");
float  rough   = ch("roughness");
float  lacuna  = ch("lacunarity");
int    octaves = chi("octaves");

vector sample_p = (@P + offset) * freq;
float sum = 0;
float contribution = 1.0;

for (int i=0; i<=octaves; i++) {
    sum += fit(noise(sample_p), 0, 1, -0.5, 0.5) * contribution;
    sample_p *= lacuna;
    contribution *= rough;
}

@P.y = sum * amp;
