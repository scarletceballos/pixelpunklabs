import bpy
import sys
import os

# Add Blender's Python modules to path
blend_paths = [
    "/Applications/Blender.app/Contents/Resources/4.2/python/lib/python3.11/site-packages",
    "/Applications/Blender.app/Contents/Resources/4.2/python/lib/site-packages",
    "/Applications/Blender.app/Contents/Resources/4.2/scripts/modules"
]

for path in blend_paths:
    if path not in sys.path:
        sys.path.append(path)

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate_model():
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        
        # Clear existing objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()
        
        # Create a simple cube
        bpy.ops.mesh.primitive_cube_add()
        
        # Save the file
        output_file = f"output_{hash(prompt)}.blend"
        bpy.ops.wm.save_as_mainfile(filepath=output_file)
        
        return jsonify({
            "success": True,
            "message": f"Created model from prompt: {prompt}",
            "file": output_file
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)