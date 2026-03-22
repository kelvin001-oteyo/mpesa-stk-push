import { useState } from "react";
import axios from "axios";

function App() {
  const [phone, setPhone] = useState("");
  const [amount, setAmount] = useState("");

  const handlePayment = async () => {
    try {
      const response = await axios.post("http://localhost:8000/stkpush/", {
        phone: phone.startsWith("0") ? "254" + phone.slice(1) : phone,
        amount: parseInt(amount),
      });
      alert(response.data.message);
    } catch (error) {
      console.error(error);
      alert("Payment failed. Check console for details.");
    }
  };

  return (
    <div>
      <h1>M-Pesa Payment</h1>
      <input
        type="text"
        placeholder="Enter phone number"
        value={phone}
        onChange={(e) => setPhone(e.target.value)}
      />
      <input
        type="number"
        placeholder="Enter amount"
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
      />
      <button onClick={handlePayment}>LIPIA SASA</button>
    </div>
  );
}

export default App;
