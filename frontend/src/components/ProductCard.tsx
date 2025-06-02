import React from 'react';
import type { Product } from '../types/product';
import { useCart } from '../context/CartContext';

interface ProductCardProps {
    product: Product;
}

const ProductCard: React.FC<ProductCardProps> = ({ product }) => {
    const defaultImageUrl = 'https://via.placeholder.com/200x150?text=Sem+Imagem';
    const { addToCart } = useCart();

    const numericPrice = parseFloat(product.price as any);
    const formattedPrice = !isNaN(numericPrice)
        ? numericPrice.toFixed(2).replace('.', ',')
        : 'Preço Indisponível';

    return (
        <div className="bg-white rounded-lg shadow-md overflow-hidden transform transition-transform duration-200 hover:scale-105">
            <img
                src={product.image || defaultImageUrl}
                alt={product.name}
                className="w-full h-48 object-cover"
            />

            <div className="p-4">
                <h3 className="text-xl font-semibold text-gray-800 mb-2 truncate">
                    {product.name}
                </h3>

                <p className="text-gray-900 text-2xl font-bold mb-4">
                    R$ {formattedPrice}
                </p>

                { }
                <button
                    onClick={() => addToCart(product)}
                    className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-75"
                >
                    Adicionar ao Carrinho
                </button>
            </div>
        </div>
    );
};

export default ProductCard;