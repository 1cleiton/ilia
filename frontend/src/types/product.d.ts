export interface Product {
    id: string;
    name: string;
    price: number;
    image: string;
    description?: string;
}

export interface CartItem extends Product {
    quantity: number;
}

interface CartItem {
    id: string;
    name: string;
    price: number;
    quantity: number;
    image: string;
}