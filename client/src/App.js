import { useState, useEffect } from "react";
import React from "react";
import image from "./Assets/Images/bg.png";
import { DropzoneArea } from 'material-ui-dropzone';
import Header from "./components/Header";
import Info from "./components/Info";
import SelectBox from "./components/SelectBox";
import axios from "axios";
import { makeStyles } from '@mui/styles';

import { Button, Container, Grid, Card, CardActionArea, CardMedia, Typography, CircularProgress, CardContent } from "@mui/material"

import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';


const useStyles = makeStyles({
	defaultButton: {
		width: "250px",
		borderRadius: "15px",
		padding: "8px",
		color: "#000000a6",
		fontSize: "20px",
		fontWeight: 900,
		// marginLeft: "32px",
		marginTop: "12px !important"
	},

	gridContainer: {
		display: "flex",
		alignItems: "center",
		flexDirection: "column !important",
		justifyContent: "start",
		padding: "1em 1em 0 1em",
		maxWidth: "400px",
	},
	label: {
		color: "#fff",
		fontSize: "18px"
	},
	mainContainer: {
		justifyContent: "center",
		backgroundImage: `url(${image})`,
		backgroundRepeat: 'no-repeat',
		backgroundPosition: 'center',
		backgroundSize: 'cover',
		height: "88vh",
		display: "flex !important"

	},
	imageCard: {
		// marginLeft: "32px",
		maxWidth: 300,
		height: 320,
		backgroundColor: 'transparent',
		boxShadow: '0px 9px 70px 0px rgb(0 0 0 / 30%) !important',
		borderRadius: '15px',
		marginTop: "16px"
	},
	imageCardEmpty: {
		height: '300px',
	},
	noImage: {
		margin: "auto",
	},
	input: {
		display: 'none',
	},
	uploadIcon: {
		background: 'white',
	},

	appbar: {
		background: '#3f51b5',
		boxShadow: 'none',
		color: 'white'
	},
	detail: {
		backgroundColor: 'white',
		display: 'flex',
		justifyContent: 'center',
		flexDirection: 'column',
		alignItems: 'center',
	},
});

function App() {
	const classes = useStyles();
	const [selectedFile, setSelectedFile] = useState();
	const [preview, setPreview] = useState();
	const [data, setData] = useState(null);
	const [image, setImage] = useState(false);
	const [plant, setPlant] = useState('');
	const [isLoading, setIsloading] = useState(false);


	const sendFile = async () => {
		if (plant === "") {
			toast.error("Vui lòng chọn loại cây trồng", {
				position: "top-center",
				autoClose: 500,
				hideProgressBar: true,
				closeOnClick: true,
				pauseOnHover: false,
				draggable: true,
				progress: undefined,
				theme: "light",
			});
			return;
		}
		if (image) {
			setIsloading(true);
			let formData = new FormData();
			formData.append("file", selectedFile);
			let res = await axios.post(`${process.env.REACT_APP_API_URL}/predict/?name=${plant}`, formData);
			if (res.status === 200) {
				setData(res.data)
			} else {
				setData(null)
			}
			setIsloading(false);
		}
	}


	const clearData = () => {
		setData(null);
		setImage(false);
		setSelectedFile(null);
		setPreview(null);
		setPlant('')
	};

	useEffect(() => {
		if (!selectedFile) {
			setPreview(undefined);
			return;
		}
		const objectUrl = URL.createObjectURL(selectedFile);
		setPreview(objectUrl);
	}, [selectedFile]);

	const getDisease = (() => {
		if (!preview) {
			return;
		}

		sendFile();
	});

	const onSelectFile = (files) => {
		if (!files || files.length === 0) {
			setSelectedFile(undefined);
			setImage(false);
			setData(undefined);
			return;
		}
		setSelectedFile(files[0]);
		setData(undefined);
		setImage(true);
	};
	return (
		<React.Fragment>
			<Header />

			<Container maxWidth={true} className={classes.mainContainer} disableGutters={true}>
				<Grid item className={classes.gridContainer}>
					<SelectBox plant={plant} setPlant={setPlant} classes={classes} />
					<Card className={`${classes.imageCard} ${!image ? classes.imageCardEmpty : ''}`}>
						{image && <CardActionArea>
							<CardMedia
								style={{ height: 250, width: 300, objectFit: "cover" }}
								image={preview}
								component="image"
								title="Contemplative Reptile"
							/>
						</CardActionArea>}
						{!image && <CardContent className={classes.content}>
							<DropzoneArea
								acceptedFiles={['image/*']}
								dropzoneText={"Kéo và thả hình ảnh lá của cây vào đây hoặc nhấp để chọn hình ảnh"}
								onChange={onSelectFile}
							/>

						</CardContent>}

						{data && <CardContent className={classes.detail}>
							<Typography style={{ marginTop: "-12px" }} variant="h6" component="div">Kết quả: {data.name}({data.confidence}%)</Typography>
							<Typography variant="h6" component="div">Độ chính xác: </Typography>

						</CardContent>}
						{isLoading && <CardContent className={classes.detail} style={{ flexDirection: "row" }}>
							<CircularProgress color="secondary" style={{ color: '#3f51b5 !important' }} />
							<Typography className={classes.title} variant="h6" noWrap>
								Đang xữ lý
							</Typography>
						</CardContent>}
					</Card>
					{data && <Button variant="contained" className={classes.defaultButton} color="primary" component="span" size="large" onClick={clearData}>
						Xóa ảnh
					</Button>}
					{!data && <Button variant="contained" className={classes.defaultButton} color="primary" component="span" size="large" onClick={(e) => { getDisease() }}>
						Kiểm tra
					</Button>}
				</Grid>
				<Grid>

					{data && <Info data={data} />}
				</Grid>
			</Container>
			<ToastContainer />
		</React.Fragment>
	);
}

export default App;
