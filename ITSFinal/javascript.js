document.getElementById("calculateBtn").addEventListener("click", function () {
    const shape = document.getElementById("shape").value;
    const parameters = {
      base: document.getElementById("base").value,
      height: document.getElementById("height").value,
    };
  
    fetch("/calculate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ shape, parameters }),
    })
      .then((response) => response.json())
      .then((data) => {
        document.getElementById("result").textContent = `Area: ${data.area}`;
      });
  });
  