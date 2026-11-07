"""Run in Rhino 8 Python 3 to import selected.json using RhinoCommon.
All coordinates are relative u. Do not assign metres without a design decision.
This import script is supplied for editing; it was not run inside Rhino desktop.
"""
import json
import Rhino
import rhinoscriptsyntax as rs
import scriptcontext as sc

# PARAMETERS: change file path through the file picker; keep study scale at 1.
STUDY_SCALE = 1.0

def rings(g):
    kind = g['type']
    if kind == 'Polygon':
        return g['coordinates']
    if kind == 'MultiPolygon':
        return [r for p in g['coordinates'] for r in p]
    if kind == 'LineString':
        return [g['coordinates']]
    if kind == 'MultiLineString':
        return g['coordinates']
    return []

def add_geometry(g, name):
    if not rs.IsLayer(name):
        rs.AddLayer(name)
    idx = sc.doc.Layers.FindByFullPath(name, -1)
    attributes = Rhino.DocObjects.ObjectAttributes()
    attributes.LayerIndex = idx
    for ring in rings(g):
        points = [Rhino.Geometry.Point3d(x*STUDY_SCALE,y*STUDY_SCALE,0) for x,y in ring]
        sc.doc.Objects.AddCurve(Rhino.Geometry.PolylineCurve(points), attributes)

path = rs.OpenFileName('Choose design/selected.json', 'JSON (*.json)|*.json||')
if path:
    with open(path, encoding='utf-8') as stream:
        data = json.load(stream)
    for u in data['units']:
        add_geometry(u['envelope'], 'Motifs')
    for key in ['floor','courts','holes','overlap','triples','routes']:
        add_geometry(data[key], key)
    sc.doc.Views.Redraw()
