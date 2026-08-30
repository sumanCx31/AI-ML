async function predictPrice() {
      const bedrooms = document.getElementById("bedrooms").value;
      const bathrooms = document.getElementById("bathrooms").value;
      const sqft = document.getElementById("sqft").value;
      const city = document.getElementById("city").value;
      const state = document.getElementById("state").value;
      const year_built = document.getElementById("year_built").value;
      const property_type = document.getElementById("property_type").value;
      const garage = document.getElementById("garage").value;
      const errorBox = document.getElementById("error");
      const resultBox = document.getElementById("result");

      if (!bedrooms || !bathrooms || !sqft || !year_built || !garage) {
        errorBox.style.display = "block";
        return;
      }
      errorBox.style.display = "none";

      try {
        const response = await fetch("http://127.0.0.1:8000/predict-aus", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            Bedrooms: parseInt(bedrooms),
            Bathrooms: parseInt(bathrooms),
            SqFt: parseInt(sqft),
            City: city,
            State: state,
            Year_Built: parseInt(year_built),
            Type: property_type,
            Garage: parseInt(garage)
          })
        });

        if (!response.ok) {
          throw new Error("Server response failed");
        }

        const data = await response.json();
        const audPrice = Math.max(Math.round(data.price), 0);
        const exchangeRate = 109.84;
        const nprPrice = Math.round(audPrice * exchangeRate);
        
        document.getElementById("audValue").textContent = "AUD $" + audPrice.toLocaleString("en-AU");
        document.getElementById("nprValue").textContent = "NPR " + nprPrice.toLocaleString("en-IN");
        resultBox.style.display = "block";
      } catch (err) {
        console.error("Error connecting to backend:", err);
        errorBox.textContent = "Could not connect to the backend server.";
        errorBox.style.display = "block";
      }
    }