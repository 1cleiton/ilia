
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Cookies from 'js-cookie';

const LoginPage: React.FC = () => {
    const [email, setEmail] = useState<string>('');
    const [password, setPassword] = useState<string>('');
    const [loading, setLoading] = useState<boolean>(false);
    const [message, setMessage] = useState<string | null>(null);
    const [isError, setIsError] = useState<boolean>(false);

    const navigate = useNavigate();

    const handleSubmit = async (event: React.FormEvent) => {
        event.preventDefault();

        setLoading(true);
        setMessage(null);
        setIsError(false);

        try {
            const response = await fetch('http://localhost:8001/api/v1/auth/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password }),
            });

            if (response.ok) {
                const data = await response.json();
                const token = data.token;

                if (token) {

                    Cookies.set('authToken', token, { expires: 7, secure: true, sameSite: 'Strict' }); // Expira em 7 dias, seguro (HTTPS), SameSite Strict
                    setMessage('Login realizado com sucesso!');
                    setIsError(false);
                    console.log('Login bem-sucedido. Token salvo nos cookies:', token);


                    navigate('/products');
                } else {
                    setMessage('Login bem-sucedido, mas nenhum token foi recebido.');
                    setIsError(true);
                }
            } else {
                const errorData = await response.json();
                setMessage(`Erro no login: ${errorData.detail || 'Credenciais inválidas'}`);
                setIsError(true);
                console.error('Erro no login:', errorData);
            }
        } catch (error) {
            setMessage('Erro ao conectar com o servidor. Tente novamente mais tarde.');
            setIsError(true);
            console.error('Erro de conexão:', error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gray-100 flex items-center justify-center">
            <div className="bg-white p-8 rounded shadow-md w-full max-w-md">
                <h2 className="text-2xl font-semibold mb-6 text-gray-800 text-center">Login</h2>

                {message && (
                    <div className={`mb-4 p-3 rounded text-sm ${isError ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'}`}>
                        {message}
                    </div>
                )}

                <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                        <label htmlFor="email" className="block text-gray-700 text-sm font-bold mb-2">
                            Email
                        </label>
                        <input
                            type="email"
                            id="email"
                            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                            placeholder="Seu email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            disabled={loading}
                        />
                    </div>
                    <div>
                        <label htmlFor="password" className="block text-gray-700 text-sm font-bold mb-2">
                            Senha
                        </label>
                        <input
                            type="password"
                            id="password"
                            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                            placeholder="Sua senha"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            disabled={loading}
                        />
                    </div>
                    <div className="flex items-center justify-between">
                        <button
                            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline disabled:opacity-50 disabled:cursor-not-allowed"
                            type="submit"
                            disabled={loading}
                        >
                            {loading ? 'Entrando...' : 'Entrar'}
                        </button>
                        <a href="#" className="inline-block align-baseline font-semibold text-sm text-blue-500 hover:text-blue-800">
                            Esqueceu a senha?
                        </a>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default LoginPage;