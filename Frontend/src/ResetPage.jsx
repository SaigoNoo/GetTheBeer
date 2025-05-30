import {useState} from "react";

export default function ContactForm() {
    const [form, setForm] = useState({
        nom: "",
        email: "",
        message: "",
    });

    const handleChange = (e) => {
        setForm({...form, [e.target.name]: e.target.value});
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log("Formulaire envoyé :", form);
        // tu peux envoyer les données ici avec fetch ou axios
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-100">
            <form
                onSubmit={handleSubmit}
                className="bg-white p-6 rounded-2xl shadow-md w-full max-w-md space-y-4"
            >
                <h2 className="text-2xl font-bold">Contacte-moi</h2>

                <input
                    type="text"
                    name="nom"
                    placeholder="Ton nom"
                    value={form.nom}
                    onChange={handleChange}
                    className="w-full p-2 border rounded-xl"
                    required
                />

                <input
                    type="email"
                    name="email"
                    placeholder="Ton email"
                    value={form.email}
                    onChange={handleChange}
                    className="w-full p-2 border rounded-xl"
                    required
                />

                <textarea
                    name="message"
                    placeholder="Ton message"
                    value={form.message}
                    onChange={handleChange}
                    className="w-full p-2 border rounded-xl"
                    rows="4"
                    required
                />

                <button
                    type="submit"
                    className="w-full bg-blue-600 text-white py-2 rounded-xl hover:bg-blue-700 transition"
                >
                    Envoyer
                </button>
            </form>
        </div>
    );
}