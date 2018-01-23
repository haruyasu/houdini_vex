# Value
$FF = @Frame
$PT = @ptnum
$PR = @primnum
$NPT = @ptnum

# Array
float test[] = {0,1,2,3,4,5}
or
f[]@test = {0,1,2,3,4,5}

# loop
f[]@test;
for(int i = 0; i<10; i++ ) {
    push(@test ,i)
}

# List Match
int idlist[];
idlist = {1523,145,1738,1739,1743,1755,1756,159,1711,204,205,211,152,151,1742,1715,1706};
if(find(idlist,@id)>=0) {
    @Cd = {0,1,0};
}

# Condition Match
int condition = (@P.x>0) ? 1:0;

# example of just adding noise(possibly shorter?)
@P=set(@P[0] , noise(set(@P[0],0,@P[2])) , @P[2]);

# Using Channel
Just use ch("parm")

# Importing point attribute from other slot
@P = point(@OpInput2,"P",@ptnum);
    or
@P = point(1,"P",@ptnum);
    or
@P = @opinput1_P;

@P.y = point(@OpInput2,"test",@ptnum);

@P = point("op:../box3","P",@ptnum);

# Attribute Variable Mapping
f@test = 1;
addvariablename(geoself(), "test", "TEST");

Intrinsic(float value is not supported yet)
i@test = primintrinsic(0,"typeid",@primnum);

# Changing Intrinsic Attribute
setattrib(geoself(), "primintrinsic", "volumebordertype", @primnum, -1, "constant", "set");
setattrib(geoself(), "primintrinsic", "volumebordervalue", @primnum, -1, 0.0, "set");

# Mix
@Cd = lerp({1,0,0},{0,1,0},0.5);
 or
v@secondP = point(@OpInput2, “P”, @ptnum);
@P = lerp(@P, @secondP, ch(“amp”));

# Centroid
vector min, max;
getbbox(min,max);
vector center = (min+max)/2;
getbbox(1,min,max);
    can get from other input

# Point Cloud
pcopen(@OpInput2, "P", @P, $radius, $maxpoints)
pcfilter($handle, $channel)
pcnumfound($handle)
pciterate($handle)

# Find nearpoint
int handle = pcopen(0, "P", @P, 2, 5); // find 5 points whitin 2 units
int otherID;
while (pciterate(handle)) {
    pcimport(handle, "point.number", otherID);
    push(@array, otherID);
}
pcclose(handle);

or
int nears = nearpoints(0,@P,10,2); // find 2 points within 10 units
foreach (int i ; nears) {
    if (@ptnum==i)
        continue;
    @near = i;
}


# Format
int handle = pcopen(@OpInput2, "P", @P, 1000, 1);
@v = pcfilter(handle, "v");
pcclose(handle);

# Loop
while (pciterate(handle)){

}

# Loop
int closept[] = pcfind(1,"P",@P, 0.5,10);

foreach (int pt; closept) {
    test += point(1, "test", pt);
}


# SDF push
float volsample = volumesample(1, 0, @P);
vector volumegrad = volumegradient(1, 0, @P);

vector pushOut = volumegrad * -volsample;
@P = @P + pushOut;


# Noise
vector freq = {1,1,1};
vector offset = {0,0,0};
float amp = 0;
int turb = 5;
float rough = 0.5;
float atten = 1;
onoise(@P*freq - offset, turb, rough, atten) * amp
snoise(@P*freq - offset, turb, rough, atten) * amp
anoise(@P*freq - offset, turb, rough, atten) * amp

vop_correctperlinNoiseVF(@P*freq - offset, turb, rough, atten) * amp
vop_correctperlinNoiseVV(@P*freq - offset, turb, rough, atten) * amp
vop_simplexNoiseVF(@P*freq - offset, turb, rough, atten) * amp
vop_simplexNoiseVV(@P*freq - offset, turb, rough, atten) * amp
vop_perlinNoiseVF(@P*freq - offset, turb, rough, atten) * amp
vop_perlinNoiseVV(@P*freq - offset, turb, rough, atten) * amp


# Remove Points(need to be cleaned. prims still exist)
if (@P.y<0){
    removepoint(geoself(), @ptnum);
}

# Remove by NDC
vector ndc=toNDC("/obj/cam1",@P);
float ov = 0;
@Cd = ndc;
if(ndc[0]-ov<0 || ndc[0]+ov>1 || ndc[1]-ov<0 || ndc[1]+ov>1 || ndc[2]>0){
    removepoint(geoself(),@ptnum);
}

# Remove Prim
if (@numvtx!=4){
    removeprim(geoself(), @primnum, 1);
}

# Remove  by vertex UV
if(@uv.x<0.5){
int prim = vertexprim( 0, @vtxnum );
removeprim( 0, prim, 1);
}

# Create centre Point(Detail)
vector min, max;
getbbox(min, max);
vector centre = (min+max)/2;
for( int i=0; i<npoints(@OpInput1); i++ ){
    removepoint(geoself(), i);
}
int centPoint = addpoint(geoself(),centre);


# Line to next Point
int a = addprim(geoself(), "polyline");
addvertex(geoself(), a, @ptnum);
addvertex(geoself(), a, @ptnum+1);

# Adding Point and Line\
int pp = addpoint(geoself(), @P + set(0,1,0) );
int a = addprim(geoself(), "polyline");
addvertex(geoself(), a, @ptnum);
addvertex(geoself(), a, pp);

# For Loop
for( int i=0; i<10; i++ ){
    int pp = addpoint(geoself(), set(0,i,0) );
}

# Neighbour Loop
f@A = 0;
for( int i=0; i<neighbourcount(0, @ptnum); i++ ){
    int np = neighbour(0,@ptnum,i);
    @A += point(0,"attr", np);
}

# Resample (prim)
int segment = 50;

for( int i=0; i<=segment; i++ ){
    vector a = primuv(0, "P", @primnum, set(float(i)/segment,0));
    int pp = addpoint(geoself(), a );
    addvertex(geoself(), @primnum, pp);
}

for( int i=0; i<primvertexcount(0, @primnum); i++ ){
    removepoint(geoself(), primpoint(0, @primnum, i));
}

# Copy
node = hou.pwd()
geo = node.geometry()

geo2 = node.inputs()[1].geometry()

uniqueName = geo2.findPointAttrib("name").strings()

cpGeoList = {}
for i in uniqueName:
    cpGeo = hou.Geometry()
    cpGeo.merge(geo)

    prims = [p for p in cpGeo.prims() if p.attribValue("name") != i]
    cpGeo.deletePrims(prims)

    cpGeoList[i] = cpGeo

tempGeo = hou.Geometry()
for i in geo2.points():
    cpName = i.attribValue("name")
    tempGeo.merge( cpGeoList[cpName] )

geo.deletePrims(geo.prims())
geo.merge(tempGeo)


-----------
***python

node = hou.pwd()
geo = node.geometry()

# Add code to modify contents of geo.
# Use drop down menu to select examples.


#create attributes on geometry
block_type = geo.addAttrib(hou.attribType.Point, "block_type", "")
point_color = geo.addAttrib(hou.attribType.Point, "Cd", (0.0, 0.0, 0.0))


#fetch pointgroups on geometry
point_groups = geo.pointGroups()

#find CBD_group, set color to red, and add to list
cbd_group = []

for group in point_groups:
    if group.name() == "CBD_group":
        for point in group.points():
            point.setAttribValue("Cd", (1.0, 0.0, 0.0))
            cbd_group.append(point.number())

#set block type attribute
for point in geo.points():
    if point.number() in cbd_group:
        point.setAttribValue("block_type", "commercial")
    elif point.number() not in cbd_group:
        point.setAttribValue("block_type", "houses")
    else:
        pass

------------
node = hou.pwd()
geo = node.geometry()

# Add code to modify contents of geo.
# Use drop down menu to select examples.


#create orignial block position attribute
original_block_pos = geo.addAttrib(hou.attribType.Point, "original_block_pos", (0.0, 0.0, 0.0))


#set original block pos for each point and move to center
for point in geo.points():
    position = point.position()
    point.setAttribValue("original_block_pos", position)
    center = (0.0, 0.0, 0.0)
    point.setPosition(center)

--------
import random

node = hou.pwd()
geo = node.geometry()

#get block type and set cluster import switch
block_type = "undefined"
block_type_num = -1

for point in geo.points():
    block_type = point.attribValue("block_type")

if block_type == "houses":
    block_type_num = 0
elif block_type == "commercial":
    block_type_num = 1
else:
    pass

hou.node("../switch_cluster_type").parm("input").set(block_type_num)


#generate random number between 0 and 2, and set building cluster switch
random_num = (random.randint(0,2))

hou.node("../../building_clusters/switch_houses_cluster").parm("input").set(random_num)
hou.node("../../building_clusters/switch_commercial_cluster").parm("input").set(random_num)

------------
node = hou.pwd()
geo = node.geometry()

# Add code to modify contents of geo.
# Use drop down menu to select examples.

block_file = hou.node(".").parm("file").eval()
block_file_path = hou.node("/out/city_block_output").parm("sopoutput").eval()


file = open(str(block_file), "a")

file.write(str(block_file_path) +"\n")

file.close
-----------
import hou
import math

node = hou.pwd()
geo = node.geometry()

#get height data for each building segment
building_height_dict = {}

children = hou.node("/obj/buildings").children()

for node in children:
    if "attribcreate" in node.name():
         building_id = node.parm("value1v1").eval()
         building_height = node.parm("value2v1").eval()
         building_height_dict[int(building_id)] = float(building_height)


#prepare base pointcloud
for point in geo.points():

    #retrieve attribute values
    building_id = point.attribValue("building_id")
    building_id_mid = building_id + 1
    building_id_top = building_id + 2
    building_height = point.attribValue("building_height")
    N = point.attribValue("N")
    up = point.attribValue("up")

    #set height values
    if building_id > 10:
        min_height = building_height_dict[building_id] + building_height_dict[building_id_mid] + building_height_dict[building_id_top]
    else:
        min_height = building_height_dict[building_id]

    skyline_height = point.attribValue("skyline_height")
    total_height = building_height

    if min_height > skyline_height:
        skyline_height = min_height


    #retrieve position data and calculate number of building segments
    position = point.position()
    number_of_building_copies = int(math.floor(skyline_height/building_height))

    counter = 0

    #create new points on stackable buildings and set attributes accordingly
    if building_id > 10:
        for each in range(number_of_building_copies):
            while total_height < skyline_height - building_height_dict[building_id_top]:

                #first mid section
                if counter == 0:

                    new_point = geo.createPoint()
                    building_id = building_id_mid

                    new_point.setAttribValue("building_id", building_id)
                    new_point.setAttribValue("building_height", float(building_height_dict[building_id]))
                    new_point.setAttribValue("skyline_height", skyline_height)
                    new_point.setAttribValue("up", up)
                    new_point.setAttribValue("N", N)

                    mid_segment_height = float(building_height_dict[building_id])
                    position = position[0], position[1] + building_height, position[2]
                    new_point.setPosition(position)
                    total_height += mid_segment_height

                    counter += 1

                #second and onwards mid sections
                elif counter > 0:

                    new_point = geo.createPoint()
                    building_id = building_id_mid

                    new_point.setAttribValue("building_id", building_id)
                    new_point.setAttribValue("building_height", float(building_height_dict[building_id]))
                    new_point.setAttribValue("skyline_height", skyline_height)
                    new_point.setAttribValue("up", up)
                    new_point.setAttribValue("N", N)

                    mid_segment_height = float(building_height_dict[building_id])
                    position = position[0], position[1] + mid_segment_height, position[2]
                    new_point.setPosition(position)
                    total_height += mid_segment_height

                    counter += 1

            #top section
            else:

                new_point = geo.createPoint()
                building_id = building_id_top

                new_point.setAttribValue("building_id", building_id)
                new_point.setAttribValue("building_height", float(building_height_dict[building_id]))
                new_point.setAttribValue("skyline_height", skyline_height)
                new_point.setAttribValue("up", up)
                new_point.setAttribValue("N", N)

                top_segment_height = float(building_height_dict[building_id])
                position = position[0], position[1] + mid_segment_height, position[2]
                new_point.setPosition(position)
                total_height += top_segment_height

                counter += 1

                break

--------------
python make geometry

# Python node example
# all python code runs only once

# create a basic geometry

# grab self geometry index
node = hou.pwd()
geo = node.geometry()

# create 4 points and remember their names
p0 = geo.createPoint()
p1 = geo.createPoint()
p2 = geo.createPoint()
p3 = geo.createPoint()
p4 = geo.createPoint()
# edit their position values
p0.setPosition((0,0,0))
p1.setPosition((.5,.5,.5))
p2.setPosition((.5,-.5,-.5))
p3.setPosition((-.5,.5,-.5))
p4.setPosition((-.5,-.5,.5))

# define a funciton to create triangels
def addTriangle(p,q,r):
 # create polygon of 3 corners
 f = geo.createPolygon()
 f.addVertex(p)
 f.addVertex(q)
 f.addVertex(r)

# create triangles inbetween the points
addTriangle(p0,p1,p2)
addTriangle(p0,p1,p3)
addTriangle(p0,p1,p4)
addTriangle(p0,p2,p3)
addTriangle(p0,p2,p4)
addTriangle(p0,p3,p4)

-------------
