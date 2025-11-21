import { useState, useEffect } from 'react';
import './PaperTrading.css';

interface Holding {
    symbol: string;
    quantity: number;
    avg_price: number;
    current_price: number;
    current_value: number;
    pnl: number;
    pnl_percent: number;
}

interface AccountData {
    balance: number;
    portfolio_value: number;
    total_equity: number;
    holdings: Holding[];
}

export default function PaperTrading() {
    const [accountData, setAccountData] = useState<AccountData | null>(null);
    const [orderSymbol, setOrderSymbol] = useState('RELIANCE.NS');
    const [orderQuantity, setOrderQuantity] = useState(1);
    const [orderSide, setOrderSide] = useState<'BUY' | 'SELL'>('BUY');
    const [orderStatus, setOrderStatus] = useState('');

    useEffect(() => {
        fetchAccountData();
    }, []);

    const fetchAccountData = async () => {
        try {
            const res = await fetch(`${import.meta.env.VITE_API_URL || ''}/api/trading/account`);
            const data = await res.json();
            setAccountData(data);
        } catch (error) {
            console.error('Failed to fetch account data, using mock data:', error);
            // Use mock data if API is not available
            setAccountData({
                balance: 100000,
                portfolio_value: 0,
                total_equity: 100000,
                holdings: []
            });
        }
    };

    const placeOrder = async () => {
        setOrderStatus('Placing order...');
        try {
            const res = await fetch(`${import.meta.env.VITE_API_URL || ''}/api/trading/order`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    symbol: orderSymbol,
                    side: orderSide,
                    quantity: orderQuantity
                })
            });

            const result = await res.json();

            if (result.status === 'success') {
                setOrderStatus(`✅ ${result.message}`);
                fetchAccountData(); // Refresh account data
            } else {
                setOrderStatus(`❌ ${result.message}`);
            }
        } catch (error) {
            setOrderStatus(`❌ Error: ${error}`);
        }
    };

    if (!accountData) {
        return <div className="loading">Loading account data...</div>;
    }

    return (
        <div className="paper-trading-container">
            <h1>📊 Paper Trading</h1>

            {/* Account Summary */}
            <div className="account-summary">
                <div className="summary-card">
                    <h3>Cash Balance</h3>
                    <p className="amount">₹{accountData.balance.toLocaleString()}</p>
                </div>
                <div className="summary-card">
                    <h3>Portfolio Value</h3>
                    <p className="amount">₹{accountData.portfolio_value.toLocaleString()}</p>
                </div>
                <div className="summary-card">
                    <h3>Total Equity</h3>
                    <p className="amount total">₹{accountData.total_equity.toLocaleString()}</p>
                </div>
            </div>

            {/* Order Placement */}
            <div className="order-panel">
                <h2>Place Order</h2>
                <div className="order-form">
                    <input
                        type="text"
                        placeholder="Symbol (e.g., RELIANCE.NS)"
                        value={orderSymbol}
                        onChange={(e) => setOrderSymbol(e.target.value)}
                    />
                    <input
                        type="number"
                        placeholder="Quantity"
                        value={orderQuantity}
                        onChange={(e) => setOrderQuantity(parseInt(e.target.value))}
                        min="1"
                    />
                    <div className="order-buttons">
                        <button
                            className={`order-btn buy ${orderSide === 'BUY' ? 'active' : ''}`}
                            onClick={() => setOrderSide('BUY')}
                        >
                            BUY
                        </button>
                        <button
                            className={`order-btn sell ${orderSide === 'SELL' ? 'active' : ''}`}
                            onClick={() => setOrderSide('SELL')}
                        >
                            SELL
                        </button>
                    </div>
                    <button className="submit-order" onClick={placeOrder}>
                        Place {orderSide} Order
                    </button>
                    {orderStatus && <p className="order-status">{orderStatus}</p>}
                </div>
            </div>

            {/* Portfolio */}
            <div className="portfolio">
                <h2>Holdings</h2>
                {accountData.holdings.length === 0 ? (
                    <p className="no-holdings">No holdings yet. Place your first order!</p>
                ) : (
                    <table className="holdings-table">
                        <thead>
                            <tr>
                                <th>Symbol</th>
                                <th>Qty</th>
                                <th>Avg Price</th>
                                <th>CMP</th>
                                <th>Value</th>
                                <th>P&L</th>
                                <th>P&L %</th>
                            </tr>
                        </thead>
                        <tbody>
                            {accountData.holdings.map((holding) => (
                                <tr key={holding.symbol}>
                                    <td className="symbol">{holding.symbol}</td>
                                    <td>{holding.quantity}</td>
                                    <td>₹{holding.avg_price.toFixed(2)}</td>
                                    <td>₹{holding.current_price.toFixed(2)}</td>
                                    <td>₹{holding.current_value.toLocaleString()}</td>
                                    <td className={holding.pnl >= 0 ? 'profit' : 'loss'}>
                                        ₹{holding.pnl.toFixed(2)}
                                    </td>
                                    <td className={holding.pnl_percent >= 0 ? 'profit' : 'loss'}>
                                        {holding.pnl_percent.toFixed(2)}%
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                )}
            </div>
        </div>
    );
}
