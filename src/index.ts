export default {
  async fetch(request: Request, env: any) {
    try {
      if (request.method === "POST") {
        const formData = await request.formData();
        const userPrompt = formData.get("prompt");
        const generationType = formData.get("generationType");
        
        if (!userPrompt) {
          return new Response("Error: No prompt provided", { status: 400 });
        }

        const enhancedPrompt = `steampunk theme: ${userPrompt}, featuring brass and copper materials, mechanical gears, Victorian era aesthetics, ornate metalwork`;

        if (generationType === "image") {
          const response = await fetch(
            "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0",
            {
              method: "POST",
              headers: {
                "Authorization": `Bearer ${env.HUGGING_FACE_API_KEY}`,
                "Content-Type": "application/json",
              },
              body: JSON.stringify({ inputs: enhancedPrompt }),
            }
          );

          // ... existing image response handling ...
        } else if (generationType === "3d") {
          const blenderResponse = await fetch(
            "YOUR_BLENDER_API_ENDPOINT",
            {
              method: "POST",
              headers: {
                "Authorization": `Bearer ${env.BLENDER_API_KEY}`,
                "Content-Type": "application/json",
              },
              body: JSON.stringify({
                prompt: enhancedPrompt,
                format: formData.get("format") || "fbx",
                complexity: formData.get("complexity") || "medium"
              }),
            }
          );

          if (!blenderResponse.ok) {
            throw new Error("Failed to generate 3D model");
          }

          return new Response(await blenderResponse.blob(), {
            headers: {
              "Content-Type": "application/octet-stream",
              "Content-Disposition": `attachment; filename="steampunk_${userPrompt.replace(/\s+/g, '_')}.fbx"`
            }
          });
        }

        return new Response(`
          <!DOCTYPE html>
          <html>
            <body style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px;">
              <h1>Steampunk Asset Generator</h1>
              <form method="POST" style="margin-top: 20px;">
                <div style="margin-bottom: 20px;">
                  <label style="display: block; margin-bottom: 8px;">Generation Type:</label>
                  <select name="generationType" id="generationType" style="padding: 8px; width: 200px;" onchange="updateOptions()">
                    <option value="image">2D Image</option>
                    <option value="3d">3D Model</option>
                  </select>
                </div>

                <input type="text" name="prompt" required
                  placeholder="Enter your prompt" 
                  style="width: 300px; padding: 8px; margin-right: 10px;">

                <div id="3dOptions" style="display: none; margin-top: 10px;">
                  <select name="format" style="padding: 8px; margin-right: 10px;">
                    <option value="fbx">FBX Format</option>
                    <option value="obj">OBJ Format</option>
                    <option value="blend">Blender File</option>
                  </select>

                  <select name="complexity" style="padding: 8px;">
                    <option value="low">Low Detail</option>
                    <option value="medium">Medium Detail</option>
                    <option value="high">High Detail</option>
                  </select>
                </div>

                <button type="submit" 
                  style="padding: 8px 16px; background: #4CAF50; color: white; border: none; border-radius: 4px;">
                  Generate
                </button>
              </form>

              <script>
                function updateOptions() {
                  const type = document.getElementById('generationType').value;
                  const options = document.getElementById('3dOptions');
                  options.style.display = type === '3d' ? 'block' : 'none';
                }
              </script>
            </body>
          </html>
        `, {
          headers: { "Content-Type": "text/html" }
        });
      }

      return new Response(`
        <!DOCTYPE html>
        <html>
          <body style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px;">
            <h1>AI Image Generator</h1>
            <form method="POST" style="margin-top: 20px;">
              <input type="text" name="prompt" required
                placeholder="Enter your prompt" 
                style="width: 300px; padding: 8px; margin-right: 10px;">
              <button type="submit" 
                style="padding: 8px 16px; background: #4CAF50; color: white; border: none; border-radius: 4px;">
                Generate Image
              </button>
            </form>
            <p style="color: #666; margin-top: 10px;">Note: Limited to 3 images per minute on free tier</p>
          </body>
        </html>
      `, {
        headers: { "Content-Type": "text/html" }
      });
    } catch (error) {
      return new Response(`
        <!DOCTYPE html>
        <html>
          <body style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px;">
            <h1>Error</h1>
            <p style="color: red;">${error.message}</p>
            <a href="/" style="color: blue; text-decoration: underline;">← Back to form</a>
          </body>
        </html>
      `, {
        headers: { "Content-Type": "text/html" },
        status: 500
      });
    }
  }
};
