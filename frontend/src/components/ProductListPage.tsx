import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Cookies from 'js-cookie';
import ProductCard from './ProductCard';
import type { Product } from '../types/product';

const ProductListPage: React.FC = () => {
    const [products, setProducts] = useState<Product[] | null>(null);
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
                    const data: Product[] = await response.json();
                    const cleanedData = data.map(p => ({
                        ...p,
                        price: parseFloat(p.price as any)
                    }));
                    setProducts(cleanedData);
                } else if (response.status === 401 || response.status === 403) {
                    Cookies.remove('authToken');
                    navigate('/login');
                    setError('Sessão expirada ou não autorizada. Faça login novamente.');
                } else {
                    const errorData = await response.json();
                    setError(`Erro ao carregar produtos: ${errorData.detail || response.statusText}`);
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
        <div className="min-h-screen bg-gray-100 p-8 pt-4"> { }
            <div className="max-w-screen-xl mx-auto">
                <h1 className="text-4xl font-extrabold text-gray-800 mb-8 text-center">Nossos Produtos</h1>
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                    {products.map((product) => (
                        <ProductCard
                            key={product.id}
                            product={product}
                        />
                    ))}
                </div>
            </div>
        </div>
    );
};

export default ProductListPage;