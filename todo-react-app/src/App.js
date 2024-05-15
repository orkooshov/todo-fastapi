import { Button, Container, Text, Title, Modal, TextInput, Group, Card, ActionIcon, Checkbox } from "@mantine/core";
import { useState, useRef, useEffect } from "react";
import { MoonStars, Sun, Trash } from "tabler-icons-react";

import { MantineProvider, ColorSchemeProvider } from "@mantine/core";
import { useHotkeys, useLocalStorage } from "@mantine/hooks";
import { AuthForm } from "./auth-form";

const API = process.env.REACT_APP_API_URL;

export default function App() {
	const [tasks, setTasks] = useState([]);
	const [opened, setOpened] = useState(false);
	const [isAuthorized, setIsAuthorized] = useState(!!localStorage.getItem("token"));
	const [user, setUser] = useState(null);

	const [colorScheme, setColorScheme] = useLocalStorage({
		key: "mantine-color-scheme",
		defaultValue: "light",
		getInitialValueInEffect: true,
	});
	const toggleColorScheme = (value) => setColorScheme(value || (colorScheme === "dark" ? "light" : "dark"));

	useHotkeys([["mod+J", () => toggleColorScheme()]]);

	const taskTitle = useRef("");
	const taskDescription = useRef("");

	async function handleCheck(id) {
		const currentTask = tasks.find((task) => task.id === id);
		await fetch(API + "/api/task/" + id, {
			method: "PATCH",
			headers: {
				"Content-Type": "application/json",
				Authorization: `Bearer ${localStorage.getItem("token")}`,
			},
			body: JSON.stringify({ is_done: !currentTask.is_done, title: currentTask.title, is_favorite: !currentTask.is_favorite }),
		});
		setTasks(tasks.map((task) => (task.id === id ? { ...task, is_done: !task.is_done } : task)));
	}

	async function createTask() {
		await fetch(API + "/api/task", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				Authorization: `Bearer ${localStorage.getItem("token")}`,
			},
			body: JSON.stringify({
				title: taskTitle.current.value,
				description: taskDescription.current.value,
			}),
		});
		await loadTasks();
	}

	async function deleteTask(id) {
		await fetch(API + "/api/task/" + id, {
			method: "DELETE",
			headers: {
				"Content-Type": "application/json",
				Authorization: `Bearer ${localStorage.getItem("token")}`,
			},
		});
		await loadTasks();
	}

	async function loadTasks() {
		const response = await fetch(API + "/api/task", {
			method: "GET",
			headers: {
				"Content-Type": "application/json",
				authorization: "Bearer " + localStorage.getItem("token"),
			},
		});
		const data = await response.json();
		setTasks(data);
	}

	async function getUser() {
		const response = await fetch(API + "/api/auth/user", {
			method: "GET",
			headers: {
				"Content-Type": "application/json",
				authorization: "Bearer " + (localStorage.getItem("token") ?? ""),
			},
		});
		const data = await response.json();
		setUser(data);
	}

	function logout() {
		localStorage.removeItem("token");
		setIsAuthorized(false);
	}

	useEffect(() => {
		if (isAuthorized) {
			loadTasks();
		}
	}, [isAuthorized]);

	useEffect(() => {
		getUser();
	}, [isAuthorized]);
	return (
		<ColorSchemeProvider colorScheme={colorScheme} toggleColorScheme={toggleColorScheme}>
			<MantineProvider theme={{ colorScheme, defaultRadius: "md" }} withGlobalStyles withNormalizeCSS>
				{isAuthorized ? (
					<div className='App'>
						<Modal
							opened={opened}
							size={"md"}
							title={"New Task"}
							withCloseButton={false}
							onClose={() => {
								setOpened(false);
							}}
							centered
						>
							<TextInput mt={"md"} ref={taskTitle} placeholder={"Task Title"} required label={"Title"} />
							<TextInput ref={taskDescription} mt={"md"} placeholder={"Task Subtask"} label={"Description"} />
							<Group mt={"md"} position={"apart"}>
								<Button
									onClick={() => {
										setOpened(false);
									}}
									variant={"subtle"}
								>
									Cancel
								</Button>
								<Button
									onClick={() => {
										createTask();
										setOpened(false);
									}}
								>
									Create Task
								</Button>
							</Group>
						</Modal>
						<Container size={750} my={40}>
							<Group position={"apart"}>
								<Title
									sx={(theme) => ({
										fontFamily: `Greycliff CF, ${theme.fontFamily}`,
										fontWeight: 900,
									})}
								>
									Welcome, {user?.first_name}!
								</Title>
								<Group>
									<Button onClick={logout}>Logout</Button>
									<ActionIcon color={"blue"} onClick={() => toggleColorScheme()} size='lg'>
										{colorScheme === "dark" ? <Sun size={16} /> : <MoonStars size={16} />}
									</ActionIcon>
								</Group>
							</Group>
							{tasks.length > 0 ? (
								tasks.map((task, index) => {
									if (task.title) {
										return (
											<Card withBorder key={index} mt={"sm"}>
												<Group position={"apart"}>
													<Text weight={"bold"}>{task.title}</Text>
													<ActionIcon
														onClick={() => {
															deleteTask(task.id);
														}}
														color={"red"}
														variant={"transparent"}
													>
														<Trash />
													</ActionIcon>
												</Group>
												<Group position={"apart"}>
													<Text color={"dimmed"} size={"md"} mt={"sm"}>
														{task.description ? task.description : "No subtasks was provided for this task"}
													</Text>
													<ActionIcon>
														<Checkbox checked={task.is_done} onChange={() => handleCheck(task.id)} />
													</ActionIcon>
												</Group>
											</Card>
										);
									}
								})
							) : (
								<Text size={"lg"} mt={"md"} color={"dimmed"}>
									You have no tasks
								</Text>
							)}
							<Button
								onClick={() => {
									setOpened(true);
								}}
								fullWidth
								mt={"md"}
							>
								New Task
							</Button>
						</Container>
					</div>
				) : (
					<Container size={550} my={40}>
						<AuthForm setIsAuthorized={setIsAuthorized} />
					</Container>
				)}
			</MantineProvider>
		</ColorSchemeProvider>
	);
}
