import { TextInput, PasswordInput, Button, Badge, Text } from "@mantine/core";
import { useEffect, useState } from "react";

const API = process.env.REACT_APP_API_URL;

export function AuthForm({ setIsAuthorized }) {
	const [username, setUserName] = useState("");
	const [password, setPassword] = useState("");

	const [firstName, setFirstName] = useState("");
	const [lastName, setLastName] = useState("");
	const [midleName, setMidleName] = useState("");

	const [error, setError] = useState("");
	const [isRegister, setIsRegister] = useState(false);

	const handleSubmit = (e) => {
		e.preventDefault();
		if (isRegister) {
			return register(username, password);
		}
		login(username, password);
	};

	const login = async (username, password) => {
		try {
			const response = await fetch(API + "/api/auth/get-token", {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify({ username, password }),
			});
			const data = await response.json();

			if (!response.ok) {
				throw new Error(`Error: ${data.detail}`);
			}

			localStorage.setItem("token", data.token);
			setIsAuthorized(true);
		} catch (err) {
			console.error(err);
			setError(err.message);
		}
	};

	const register = async (username, password) => {
		try {
			const response = await fetch(API + "/api/auth/user", {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify({ username, password, first_name: firstName, last_name: lastName, middle_name: midleName }),
			});
			const data = await response.json();

			if (!response.ok) {
				throw new Error(`Error: ${data.detail}`);
			}

			localStorage.setItem("token", data.token);
			setIsAuthorized(true);
		} catch (err) {
			console.error(err);
			setError(err.message);
		}
	};

	return (
		<form>
			<Text mb={"md"} style={{ fontSize: 32, fontWeight: 700, textAlign: "center" }}>
				{isRegister ? "Register" : "Login"}
			</Text>
			<TextInput onChange={(e) => setUserName(e.target.value)} value={username} id='username' name='username' label='Enter your username' required placeholder='Your username' />
			<PasswordInput onChange={(e) => setPassword(e.target.value)} value={password} id='password' name='password' label='Enter your password' required placeholder='Your password' mt='md' />
			{isRegister && (
				<>
					<TextInput onChange={(e) => setFirstName(e.target.value)} value={firstName} id='firstName' name='firstName' label='Enter your first name' required placeholder='Your first name' mt='md' />
					<TextInput onChange={(e) => setLastName(e.target.value)} value={lastName} id='lastName' name='lastName' label='Enter your last name' required placeholder='Your last name' mt='md' />
					<TextInput onChange={(e) => setMidleName(e.target.value)} value={midleName} id='midleName' name='midleName' label='Enter your midle name' required placeholder='Your midle name' mt='md' />
				</>
			)}

			<Button type='submit' fullWidth mt={"md"} onClick={handleSubmit}>
				{isRegister ? "Register" : "Login"}
			</Button>
			<Text style={{ textAlign: "center" }} mt={16}>
				{isRegister ? "Already have an account?" : "Don't have an account?"}
			</Text>
			<Button fullWidth mt={"md"} variant='outline' onClick={(e) => setIsRegister(!isRegister)}>
				{!isRegister ? "Register" : "Login"}
			</Button>
			{error && <Badge color='red'>{error}</Badge>}
		</form>
	);
}
