import React from 'react'
import logo from "../Assets/Images/logo.png";
import { AppBar, Toolbar, Typography, Avatar } from '@mui/material';


function Header() {

	return (
		<AppBar position="static" style={{
			background: '#3f51b5',
			boxShadow: 'none',
			color: 'white'
		}} >
			<Toolbar>
				<Typography variant="h6" noWrap>
					Phát hiện bệnh trên cây trồng
				</Typography>
				<div style={{ flexGrow: 1 }}></div>
				<Avatar src={logo}></Avatar>
			</Toolbar>
		</AppBar>
	)
}
export default Header