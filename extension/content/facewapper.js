console.log("FaceWapper content script active");

async function collectImages() {
  const images = Array.from(document.querySelectorAll("img"))
    .map(img => ({
      element: img,
      src: img.src,
      rect: img.getBoundingClientRect()
    }))
    .filter(img => img.src && !img.src.startsWith("data:") && img.rect.width > 100 && img.rect.height > 100);

  console.log(`Found ${images.length} images`);
  return images;
}

async function swapAllImages() {
  console.log("Starting face swap");

  const images = await collectImages();
  const urls = images.map(i => i.src);

  if (!urls.length) {
    console.log("No images found to swap");
    return;
  }

  console.log(`Sending ${urls.length} images to server`);

  try {
    const response = await fetch("http://127.0.0.1:5000/swap-images", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ urls })
    });

    const data = await response.json();
    console.log("Got swapped URLs:", data);

    if (data.new_urls && data.new_urls.length > 0) {
      data.new_urls.forEach((newUrl, i) => {
        if (images[i] && newUrl) {
          images[i].element.src = newUrl;
          images[i].element.srcset = newUrl;
        }
      });
    }

    console.log("Face swap complete!");

  } catch (err) {
    console.error("Error swapping faces:", err);
  }
}

swapAllImages();
