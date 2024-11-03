export default {
  async fetch(request: Request, env: any) {
    try {
      // Handle form submission (POST request)
      if (request.method === "POST") {
        const formData = await request.formData();
        const userPrompt = formData.get("prompt");
        
        if (!userPrompt) {
          return new Response("Error: No prompt provided", { status: 400 });
        }

        const enhancedPrompt = `steampunk theme: ${userPrompt}, featuring brass and copper materials, mechanical gears, Victorian era aesthetics, ornate metalwork`;

        // Call Hugging Face API
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

        if (!response.ok) {
          const error = await response.json();
          if (error.error && error.error.includes("Max requests")) {
            return new Response(`
              <!DOCTYPE html>
              <html>
                <body style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px;">
                  <h1>Rate Limit Reached</h1>
                  <p style="color: orange;">Please wait a minute before generating another image. The free tier allows 3 images per minute.</p>
                  <p>Your prompt was: "${userPrompt}"</p>
                  <a href="/" style="color: blue; text-decoration: underline;">← Back to form</a>
                </body>
              </html>
            `, {
              headers: { "Content-Type": "text/html" },
              status: 429
            });
          }
          throw new Error(error.error || "API Error");
        }

        // Return a page that displays the image
        return new Response(`
          <!DOCTYPE html>
          <html>
            <body style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px;">
              <h1>Generated Image</h1>
              <img src="data:image/jpeg;base64,${
                Buffer.from(await response.arrayBuffer()).toString('base64')
              }" style="max-width: 100%; height: auto;">
              <br>
              <p><strong>Note:</strong> Free tier limited to 3 images per minute</p>
              <a href="/" style="color: blue; text-decoration: underline; display: inline-block; margin-top: 20px;">← Generate another image</a>
            </body>
          </html>
        `, {
          headers: { "Content-Type": "text/html" }
        });
      }

      // Show the form (GET request)
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
