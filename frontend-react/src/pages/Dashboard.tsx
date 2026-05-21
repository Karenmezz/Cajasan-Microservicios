import { useEffect, useState } from "react";
import { api } from "../api/client";

interface Props {
  onLogout: () => void;
}

interface Product {
  id: number;
  name: string;
  price: number;
  stock: number;
}

interface Order {
  id: number;
  user: string;
  productId?: number;
  product_id?: number;
  quantity: number;
  total: number;
}

export default function Dashboard({ onLogout }: Props) {
  const [products, setProducts] = useState<Product[]>([]);
  const [orders, setOrders] = useState<Order[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    api
      .get<Product[]>("/products")
      .then((r) => setProducts(r.data))
      .catch(() => setError("No se pudieron cargar los productos"));
    api
      .get<Order[]>("/orders")
      .then((r) => setOrders(r.data))
      .catch(() => setError("No se pudieron cargar las ordenes"));
  }, []);

  async function handleLogout() {
    try {
      await api.post("/auth/logout");
    } catch {
      // ignore
    }
    onLogout();
  }

  return (
    <div style={{ maxWidth: 700, margin: "40px auto", fontFamily: "sans-serif" }}>
      <div style={{ display: "flex", justifyContent: "space-between" }}>
        <h2>Tienda</h2>
        <button onClick={handleLogout}>Cerrar sesion</button>
      </div>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <h3>Productos</h3>
      <ul>
        {products.map((p) => (
          <li key={p.id}>
            {p.name} - ${p.price} (stock: {p.stock})
          </li>
        ))}
      </ul>
      <h3>Ordenes</h3>
      <ul>
        {orders.map((o) => (
          <li key={o.id}>
            #{o.id} - {o.user} - cantidad {o.quantity} - total ${o.total}
          </li>
        ))}
      </ul>
    </div>
  );
}
