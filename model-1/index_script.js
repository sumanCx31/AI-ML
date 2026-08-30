
    async function predictPrice() {
      const size = document.getElementById("size").value;
      const floors = document.getElementById("floors").value;
      const age = document.getElementById("age").value;
      const location = document.getElementById("location").value;
      const errorBox = document.getElementById("error");
      const resultBox = document.getElementById("result");
      const predictBtn = document.getElementById("predictBtn");

      if (!size || !floors || !age || !location) {
        errorBox.textContent = "Please fill in all fields with valid values.";
        errorBox.style.display = "block";
        return;
      }
      errorBox.style.display = "none";
      
      predictBtn.disabled = true;
      predictBtn.textContent = "Predicting...";

      try {
        const response = await fetch("http://127.0.0.1:8000/predict-nepal", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            size: parseFloat(size),
            floors: parseFloat(floors),
            age: parseFloat(age),
            location: location
          })
        });

        if (!response.ok) {
          throw new Error("Server response failed");
        }

        const data = await response.json();
        
        document.getElementById("resultValue").textContent =
          "NPR " + Math.max(Math.round(data.price), 0).toLocaleString("en-IN");
        resultBox.style.display = "block";
      } catch (err) {
        console.error("Error connecting to backend:", err);
        errorBox.textContent = "Could not connect to the backend server.";
        errorBox.style.display = "block";
      } finally {
        predictBtn.disabled = false;
        predictBtn.textContent = "Predict Price";
      }
    }