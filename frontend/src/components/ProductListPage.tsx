import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Cookies from 'js-cookie';

const ProductListPage: React.FC = () => {
    const [products, setProducts] = useState<any[] | null>(null);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    const navigate = useNavigate();

    useEffect(() => {
        const fetchProducts = async () => {
            setLoading(true);
            setError(null);

            const token = Cookies.get('authToken');

            if (!token) {

                navigate('/login');
                return;
            }

            try {

                const response = await fetch('http://localhost:8001/api/v1/products', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Token ${token}`,

                    },
                });

                if (response.ok) {
                    const data = await response.json();
                    setProducts(data);
                    console.log('Produtos obtidos:', data);
                } else if (response.status === 401 || response.status === 403) {

                    Cookies.remove('authToken');
                    navigate('/login');
                    setError('Sessão expirada ou não autorizada. Faça login novamente.');
                } else {
                    const errorData = await response.json();
                    setError(`Erro ao carregar produtos: ${errorData.detail || response.statusText}`);
                    console.error('Erro ao carregar produtos:', errorData);
                }
            } catch (err) {
                setError('Erro de conexão ao carregar produtos.');
                console.error('Erro de rede ao carregar produtos:', err);
            } finally {
                setLoading(false);
            }
        };

        fetchProducts();
    }, [navigate]);

    const handleLogout = () => {
        Cookies.remove('authToken');
        navigate('/login');
    };

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-gray-100">
                <p className="text-xl text-gray-700">Carregando produtos...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-gray-100">
                <p className="text-xl text-red-600">Erro: {error}</p>
            </div>
        );
    }

    if (!products || products.length === 0) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-gray-100">
                <p className="text-xl text-gray-700">Nenhum produto encontrado.</p>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-100 p-8">
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-3xl font-bold text-gray-800">Lista de Produtos</h1>
                <button
                    onClick={handleLogout}
                    className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                >
                    Sair
                </button>
            </div>
            <pre className="bg-white p-4 rounded shadow-md text-sm overflow-auto max-w-4xl mx-auto">
                {JSON.stringify(products, null, 2)}
            </pre>
        </div>
    );
};

export default ProductListPage;