import React, { createContext, useContext, useState, useEffect } from 'react';
import Cookies from 'js-cookie';
import type { Product, CartItem } from '../types/product';


interface CartContextType {
    cartItems: CartItem[];
    addToCart: (product: Product) => void;
    removeFromCart: (productId: string) => void;
    clearCart: () => void;
    getTotalItems: () => number;
}


const CartContext = createContext<CartContextType | undefined>(undefined);


const CART_COOKIE_NAME = 'shoppingCart';


interface CartProviderProps {
    children: React.ReactNode;
}

export const CartProvider: React.FC<CartProviderProps> = ({ children }) => {
    const [cartItems, setCartItems] = useState<CartItem[]>(() => {
        try {
            const savedCart = Cookies.get(CART_COOKIE_NAME);
            return savedCart ? JSON.parse(savedCart) : [];
        } catch (e) {
            console.error('Falha ao carregar carrinho dos cookies:', e);
            Cookies.remove(CART_COOKIE_NAME);
            return [];
        }
    });

    useEffect(() => {
        if (cartItems.length > 0 || Cookies.get(CART_COOKIE_NAME)) {
            Cookies.set(CART_COOKIE_NAME, JSON.stringify(cartItems), {
                expires: 7,
                secure: true,
                sameSite: 'Strict',
            });
        } else {
            Cookies.remove(CART_COOKIE_NAME);
        }
    }, [cartItems]);

    const addToCart = (product: Product) => {
        setCartItems((prevItems) => {
            const existingItem = prevItems.find((item) => item.id === product.id);

            if (existingItem) {
                return prevItems.map((item) =>
                    item.id === product.id ? { ...item, quantity: item.quantity + 1 } : item
                );
            } else {
                return [...prevItems, { ...product, quantity: 1 }];
            }
        });
    };

    const removeFromCart = (productId: string) => {
        setCartItems((prevItems) => {
            const existingItem = prevItems.find((item) => item.id === productId);

            if (existingItem && existingItem.quantity > 1) {
                return prevItems.map((item) =>
                    item.id === productId ? { ...item, quantity: item.quantity - 1 } : item
                );
            } else {
                return prevItems.filter((item) => item.id !== productId);
            }
        });
    };

    const clearCart = () => {
        setCartItems([]);
    };

    const getTotalItems = () => {
        return cartItems.reduce((total, item) => total + item.quantity, 0);
    };

    const value = {
        cartItems,
        addToCart,
        removeFromCart,
        clearCart,
        getTotalItems,
    };

    return <CartContext.Provider value={value}>{children}</CartContext.Provider>;
};

export const useCart = () => {
    const context = useContext(CartContext);
    if (context === undefined) {
        throw new Error('useCart deve ser usado dentro de um CartProvider');
    }
    return context;
};