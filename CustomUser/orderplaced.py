from Order.models import Order

def make_column(lead: str, trail: str):
	return f'''
		<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-2"
								role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
								<tbody>
									<tr>
										<td>
											<table align="center" border="0" cellpadding="0" cellspacing="0"
												class="row-content stack" role="presentation"
												style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; color: #000000; width: 500px;"
												width="500">
												<tbody>
													<tr>
														<td class="column"
															style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;"
															width="25%">
															<table border="0" cellpadding="0" cellspacing="0" class="text_block"
																role="presentation"
																style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
																width="100%">
																<tr>
																	<td
																		style="padding-top:15px;padding-right:10px;padding-bottom:15px;padding-left:10px;">
																		<div style="font-family: sans-serif">
																			<div
																				style="font-size: 14px; mso-line-height-alt: 16.8px; color: #555555; line-height: 1.2; font-family: Arial, Helvetica Neue, Helvetica, sans-serif;">
																				{str(lead)}</div>
																		</div>
																	</td>
																</tr>
															</table>
														</td>
														<td class="column"
															style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;"
															width="50%">
															<table border="0" cellpadding="0" cellspacing="0" class="text_block"
																role="presentation"
																style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
																width="100%">
																<tr>
																	<td
																		style="padding-top:15px;padding-right:10px;padding-bottom:15px;padding-left:10px;">
																		<div style="font-family: sans-serif">
																			<div
																				style="font-size: 12px; mso-line-height-alt: 14.399999999999999px; color: #555555; line-height: 1.2; font-family: Arial, Helvetica Neue, Helvetica, sans-serif;">
																				<p
																					style="margin: 0; font-size: 12px; mso-line-height-alt: 14.399999999999999px;">
																					 </p>
																			</div>
																		</div>
																	</td>
																</tr>
															</table>
														</td>
														<td class="column"
															style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;"
															width="25%">
															<table border="0" cellpadding="0" cellspacing="0" class="text_block"
																role="presentation"
																style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
																width="100%">
																<tr>
																	<td
																		style="padding-top:15px;padding-right:10px;padding-bottom:15px;padding-left:10px;">
																		<div style="font-family: sans-serif">
																			<div
																				style="font-size: 14px; text-align: right; mso-line-height-alt: 16.8px; color: #555555; line-height: 1.2; font-family: Arial, Helvetica Neue, Helvetica, sans-serif;">
																				{str(trail)}</div>
																		</div>
																	</td>
																</tr>
															</table>
														</td>
													</tr>
												</tbody>
											</table>
										</td>
									</tr>
								</tbody>
							</table>
		'''

def get_order_placed_html(order: Order):
	billPortion = ''''''
	if order.user:
		billPortion += make_column(lead="User:", trail=str(order.user.profile_full_name()))
	if order.DeliveryAddress:
		billPortion += make_column(lead="Phone Number:", trail=str(order.DeliveryAddress.phone))
	if order.billNo:
		billPortion += make_column(lead="Bill No:", trail=str(order.billNo))
	if order.receiptNo:
		billPortion += make_column(lead="Receipt No:", trail=str(order.receiptNo))
	if order.grandAmount:
		billPortion += make_column(lead="Total Amount", trail="Rs. " + str(order.grandAmount))
	
	productPortion = ''''''
	for orderItem in order.items.all():
		productPortion += f'''
		<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-2"
								role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
								<tbody>
									<tr>
										<td>
											<table align="center" border="0" cellpadding="0" cellspacing="0"
												class="row-content stack" role="presentation"
												style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; color: #000000; width: 500px;"
												width="500">
												<tbody>
													<tr>
														<td class="column"
															style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;"
															width="25%">
															<table border="0" cellpadding="0" cellspacing="0" class="text_block"
																role="presentation"
																style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
																width="100%">
																<tr>
																	<td
																		style="padding-top:15px;padding-right:10px;padding-bottom:15px;padding-left:10px;">
																		<div style="font-family: sans-serif">
																			<div
																				style="font-size: 14px; mso-line-height-alt: 16.8px; color: #555555; line-height: 1.2; font-family: Arial, Helvetica Neue, Helvetica, sans-serif;">
																				{str(orderItem.item.title)}</div>
																		</div>
																	</td>
																</tr>
															</table>
														</td>
														<td class="column"
															style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;"
															width="50%">
															<table border="0" cellpadding="0" cellspacing="0" class="text_block"
																role="presentation"
																style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
																width="100%">
																<tr>
																	<td
																		style="padding-top:15px;padding-right:10px;padding-bottom:15px;padding-left:10px;">
																		<div style="font-family: sans-serif">
																			<div
																				style="font-size: 12px; mso-line-height-alt: 14.399999999999999px; color: #555555; line-height: 1.2; font-family: Arial, Helvetica Neue, Helvetica, sans-serif;">
																				<p
																					style="margin: 0; font-size: 12px; mso-line-height-alt: 14.399999999999999px;">
																					 </p>
																			</div>
																		</div>
																	</td>
																</tr>
															</table>
														</td>
														<td class="column"
															style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;"
															width="25%">
															<table border="0" cellpadding="0" cellspacing="0" class="text_block"
																role="presentation"
																style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
																width="100%">
																<tr>
																	<td
																		style="padding-top:15px;padding-right:10px;padding-bottom:15px;padding-left:10px;">
																		<div style="font-family: sans-serif">
																			<div
																				style="font-size: 14px; text-align: right; mso-line-height-alt: 16.8px; color: #555555; line-height: 1.2; font-family: Arial, Helvetica Neue, Helvetica, sans-serif;">
																				Quantity: {str(orderItem.quantity)}</div>
																		</div>
																	</td>
																</tr>
															</table>
														</td>
													</tr>
												</tbody>
											</table>
										</td>
									</tr>
								</tbody>
							</table>
		'''

	
	nulledHtml = '''<!DOCTYPE html>

		<html lang="en" xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:v="urn:schemas-microsoft-com:vml">

		<head>
			<title></title>
			<meta charset="utf-8" />
			<meta content="width=device-width, initial-scale=1.0" name="viewport" />
			<!--[if mso]><xml><o:OfficeDocumentSettings><o:PixelsPerInch>96</o:PixelsPerInch><o:AllowPNG/></o:OfficeDocumentSettings></xml><![endif]-->
			<!--[if !mso]><!-->
			<link href="https://fonts.googleapis.com/css?family=Montserrat" rel="stylesheet" type="text/css" />
			<!--<![endif]-->
			<style>
				* {
					box-sizing: border-box;
				}

				body {
					margin: 0;
					padding: 0;
				}

				a[x-apple-data-detectors] {
					color: inherit !important;
					text-decoration: inherit !important;
				}

				#MessageViewBody a {
					color: inherit;
					text-decoration: none;
				}

				p {
					line-height: inherit
				}

				@media (max-width:520px) {
					.icons-inner {
						text-align: center;
					}

					.icons-inner td {
						margin: 0 auto;
					}

					.row-content {
						width: 100% !important;
					}

					.stack .column {
						width: 100%;
						display: block;
					}
				}
			</style>
		</head>

		<body style="background-color: #FFFFFF; margin: 0; padding: 0; -webkit-text-size-adjust: none; text-size-adjust: none;">
			<table border="0" cellpadding="0" cellspacing="0" class="nl-container" role="presentation"
				style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #FFFFFF;" width="100%">
				<tbody>
					<tr>
						<td>
							<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-1"
								role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
								<tbody>
									<tr>
										<td>
											<table align="center" border="0" cellpadding="0" cellspacing="0"
												class="row-content stack" role="presentation"
												style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; color: #000000; width: 500px;"
												width="500">
												<tbody>
													<tr>
														<td class="column"
															style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; padding-top: 5px; padding-bottom: 5px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;"
															width="100%">
															<table border="0" cellpadding="10" cellspacing="0"
																class="text_block" role="presentation"
																style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
																width="100%">
																<tr>
																	<td>
																		<div
																			style="font-family: 'Trebuchet MS', Tahoma, sans-serif">
																			<div
																				style="font-size: 14px; text-align: center; font-family: 'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif; mso-line-height-alt: 16.8px; color: #555555; line-height: 1.2;">
																				<p style="margin: 0;"><span
																						style="font-size:17px;"><strong>NEW
																							ORDER HAS BEEN PLACED
																							!</strong></span></p>
																			</div>
																		</div>
																	</td>
																</tr>
															</table>
															<table border="0" cellpadding="10" cellspacing="0"
																class="divider_block" role="presentation"
																style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
																width="100%">
																<tr>
																	<td>
																		<div align="center">
																			<table border="0" cellpadding="0" cellspacing="0"
																				role="presentation"
																				style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
																				width="100%">
																				<tr>
																					<td class="divider_inner"
																						style="font-size: 1px; line-height: 1px; border-top: 1px solid #BBBBBB;">
																						<span> </span></td>
																				</tr>
																			</table>
																		</div>
																	</td>
																</tr>
															</table>
															<table border="0" cellpadding="0" cellspacing="0"
																class="image_block" role="presentation"
																style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
																width="100%">
																<tr>
																	<td style="width:100%;padding-right:0px;padding-left:0px;">
																		<div align="center" style="line-height:10px">

																			
																			<img
																				src="https://fod.suzanpradhan.com.np/media/new_order.png"
																				style="display: block; height: auto; border: 0; width: 285px; max-width: 100%;"
																				width="285" /></div>
																	</td>
																</tr>
															</table>
															<table border="0" cellpadding="10" cellspacing="0"
																class="divider_block" role="presentation"
																style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
																width="100%">
																<tr>
																	<td>
																		<div align="center">
																			<table border="0" cellpadding="0" cellspacing="0"
																				role="presentation"
																				style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
																				width="100%">
																				<tr>
																					<td class="divider_inner"
																						style="font-size: 1px; line-height: 1px; border-top: 1px solid #BBBBBB;">
																						<span> </span></td>
																				</tr>
																			</table>
																		</div>
																	</td>
																</tr>
															</table>
															<table border="0" cellpadding="10" cellspacing="0"
																class="text_block" role="presentation"
																style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
																width="100%">
																<tr>
																	<td>
																		<div
																			style="font-family: 'Trebuchet MS', Tahoma, sans-serif">
																			<div
																				style="font-size: 14px; font-family: 'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif; mso-line-height-alt: 16.8px; color: #555555; line-height: 1.2;">
																				<strong>Order Details:</strong></div>
																		</div>
																	</td>
																</tr>
															</table>
															<table border="0" cellpadding="10" cellspacing="0"
																class="divider_block" role="presentation"
																style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
																width="100%">
																<tr>
																	<td>
																		<div align="center">
																			<table border="0" cellpadding="0" cellspacing="0"
																				role="presentation"
																				style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
																				width="100%">
																				<tr>
																					<td class="divider_inner"
																						style="font-size: 1px; line-height: 1px; border-top: 1px solid #BBBBBB;">
																						<span> </span></td>
																				</tr>
																			</table>
																		</div>
																	</td>
																</tr>
															</table>
														</td>
													</tr>
												</tbody>
											</table>
										</td>
									</tr>
								</tbody>
							</table>
							'''+ billPortion +'''
							<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-7"
								role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
								<tbody>
									<tr>
										<td>
											<table align="center" border="0" cellpadding="0" cellspacing="0"
												class="row-content stack" role="presentation"
												style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; color: #000000; width: 500px;"
												width="500">
												<tbody>
													<tr>
														<td class="column"
															style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; padding-top: 5px; padding-bottom: 5px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;"
															width="100%">
															<table border="0" cellpadding="10" cellspacing="0"
																class="divider_block" role="presentation"
																style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
																width="100%">
																<tr>
																	<td>
																		<div align="center">
																			<table border="0" cellpadding="0" cellspacing="0"
																				role="presentation"
																				style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
																				width="100%">
																				<tr>
																					<td class="divider_inner"
																						style="font-size: 1px; line-height: 1px; border-top: 1px solid #BBBBBB;">
																						<span> </span></td>
																				</tr>
																			</table>
																		</div>
																	</td>
																</tr>
															</table>
															<table border="0" cellpadding="10" cellspacing="0"
																class="text_block" role="presentation"
																style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
																width="100%">
																<tr>
																	<td>
																		<div style="font-family: sans-serif">
																			<div
																				style="font-size: 14px; mso-line-height-alt: 16.8px; color: #555555; line-height: 1.2; font-family: Arial, Helvetica Neue, Helvetica, sans-serif;">
																				Products:</div>
																		</div>
																	</td>
																</tr>
															</table>
															<table border="0" cellpadding="10" cellspacing="0"
																class="divider_block" role="presentation"
																style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
																width="100%">
																<tr>
																	<td>
																		<div align="center">
																			<table border="0" cellpadding="0" cellspacing="0"
																				role="presentation"
																				style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
																				width="100%">
																				<tr>
																					<td class="divider_inner"
																						style="font-size: 1px; line-height: 1px; border-top: 1px solid #BBBBBB;">
																						<span> </span></td>
																				</tr>
																			</table>
																		</div>
																	</td>
																</tr>
															</table>
														</td>
													</tr>
												</tbody>
											</table>
										</td>
									</tr>
								</tbody>
							</table>
							'''+ productPortion +'''
						</td>
					</tr>
				</tbody>
			</table><!-- End -->
		</body>

		</html>'''

	return nulledHtml


def make_verification_email(verification_link: str, username=str):
	print(username)
	print(verification_link)
	verification_email = '''<!DOCTYPE html>

		<html lang="en" xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:v="urn:schemas-microsoft-com:vml">

		<head>
			<title></title>
			<meta charset="utf-8" />
			<meta content="width=device-width, initial-scale=1.0" name="viewport" />
			<link href="https://fonts.googleapis.com/css?family=Lato" rel="stylesheet" type="text/css" />
			<link href="https://fonts.googleapis.com/css?family=Permanent+Marker" rel="stylesheet" type="text/css" />
			<link href="https://fonts.googleapis.com/css?family=Ubuntu" rel="stylesheet" type="text/css" />
			<link href="https://fonts.googleapis.com/css?family=Montserrat" rel="stylesheet" type="text/css" />
			<link href="https://fonts.googleapis.com/css?family=Open+Sans" rel="stylesheet" type="text/css" />
			<link href="https://fonts.googleapis.com/css?family=Roboto" rel="stylesheet" type="text/css" />
			<style>
				* {
					box-sizing: border-box;
				}

				body {
					margin: 0;
					padding: 0;
				}

				a[x-apple-data-detectors] {
					color: inherit !important;
					text-decoration: inherit !important;
				}

				#MessageViewBody a {
					color: inherit;
					text-decoration: none;
				}

				p {
					line-height: inherit
				}

				@media (max-width:625px) {
					.icons-inner {
						text-align: center;
					}

					.icons-inner td {
						margin: 0 auto;
					}

					.row-content {
						width: 100% !important;
					}

					.image_block img.big {
						width: auto !important;
					}

					.stack .column {
						width: 100%;
						display: block;
					}
				}
			</style>
		</head>

		<body style="background-color: #000000; margin: 0; padding: 0; -webkit-text-size-adjust: none; text-size-adjust: none;">
			<table border="0" cellpadding="0" cellspacing="0" class="nl-container" role="presentation"
				style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #000000;" width="100%">
				<tbody>
					<tr>
						<td>
							<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-1"
								role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
								<tbody>
									<tr>
										<td>
											<table align="center" border="0" cellpadding="0" cellspacing="0"
												class="row-content stack" role="presentation"
												style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #1b1c1c; color: #000000; width: 605px;"
												width="605">
												<tbody>
													<tr>
														<td class="column"
															style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; padding-top: 5px; padding-bottom: 0px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;"
															width="100%">
															<table border="0" cellpadding="0" cellspacing="0"
																class="image_block" role="presentation"
																style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
																width="100%">
																<tr>
																	<td
																		style="width:100%;padding-right:0px;padding-left:0px;padding-top:15px;">
																		<div align="center" style="line-height:10px"><a
																				href="https://fod.suzanpradhan.com.np"
																				style="outline:none" tabindex="-1"
																				target="_blank"><img alt="Placeholder logo"
																					src="https://fod.suzanpradhan.com.np/media/email_cover.png"
																					style="display: block; height: auto; border: 0; width: 100%; max-width: 100%;"
																					title="Fodery Logo" width="70" /></a>
																		</div>
																	</td>
																</tr>
															</table>
														</td>
													</tr>
												</tbody>
											</table>
										</td>
									</tr>
								</tbody>
							</table>
							<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-2"
								role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
								<tbody>
									<tr>
										<td>
											<table align="center" border="0" cellpadding="0" cellspacing="0"
												class="row-content stack" role="presentation"
												style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #1b1c1c; color: #000000; width: 605px;"
												width="605">
												<tbody>
													<tr>
														<td class="column"
															style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; padding-top: 5px; padding-bottom: 5px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;"
															width="100%">
															<table border="0" cellpadding="10" cellspacing="0"
																class="divider_block" role="presentation"
																style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
																width="100%">
																<tr>
																	<td>
																		<div align="center">
																			<table border="0" cellpadding="0" cellspacing="0"
																				role="presentation"
																				style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
																				width="100%">
																				<tr>
																					<td class="divider_inner"
																						style="font-size: 1px; line-height: 1px; border-top: 2px solid #252626;">
																						<span> </span></td>
																				</tr>
																			</table>
																		</div>
																	</td>
																</tr>
															</table>
															<table border="0" cellpadding="10" cellspacing="0"
																class="text_block" role="presentation"
																style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
																width="100%">
																<tr>
																	<td>
																		<div
																			style="font-family: 'Trebuchet MS', Tahoma, sans-serif">
																			<div
																				style="font-family: 'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif; font-size: 12px; mso-line-height-alt: 14.399999999999999px; color: #ffffff; line-height: 1.2;">
																				<p
																					style="margin: 0; font-size: 14px; text-align: center;">
																					<span style="font-size:24px;"><strong>Email
																							Verification</strong></span></p>
																			</div>
																		</div>
																	</td>
																</tr>
															</table>
															<table border="0" cellpadding="10" cellspacing="0"
																class="divider_block" role="presentation"
																style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
																width="100%">
																<tr>
																	<td>
																		<div align="center">
																			<table border="0" cellpadding="0" cellspacing="0"
																				role="presentation"
																				style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
																				width="100%">
																				<tr>
																					<td class="divider_inner"
																						style="font-size: 1px; line-height: 1px; border-top: 2px solid #252626;">
																						<span> </span></td>
																				</tr>
																			</table>
																		</div>
																	</td>
																</tr>
															</table>
														</td>
													</tr>
												</tbody>
											</table>
										</td>
									</tr>
								</tbody>
							</table>
							<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-3"
								role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
								<tbody>
									<tr>
										<td>
											<table align="center" border="0" cellpadding="0" cellspacing="0"
												class="row-content stack" role="presentation"
												style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #1b1c1c; color: #000000; width: 605px;"
												width="605">
												<tbody>
													<tr>
														<td class="column"
															style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; padding-top: 0px; padding-bottom: 0px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;"
															width="100%">
															<table border="0" cellpadding="0" cellspacing="0" class="text_block"
																role="presentation"
																style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
																width="100%">
																<tr>
																	<td
																		style="padding-top:45px;padding-right:45px;padding-bottom:20px;padding-left:45px;">
																		<div
																			style="font-family: 'Trebuchet MS', Tahoma, sans-serif">
																			<div
																				style="font-size: 14px; font-family: 'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif; mso-line-height-alt: 16.8px; color: #f0f5f9; line-height: 1.2;">
																				<p style="margin: 0; font-size: 14px;">Hello
																					'''+username+''',</p>
																				<p
																					style="margin: 0; font-size: 14px; mso-line-height-alt: 16.8px;">
																					 </p>
																				<p style="margin: 0; color: #ffffff;">Thank you for joining
																					Foodery. To get access to your account
																					please verify your email address by clicking
																					the link below.</p>
																				<p style="margin: 0; color: #ffffff;">or you can activate by
																					clicking on below button.</p>
																			</div>
																		</div>
																	</td>
																</tr>
															</table>
															<table border="0" cellpadding="10" cellspacing="0"
																class="button_block" role="presentation"
																style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
																width="100%">
																<tr>
																	<td>
																		<div align="center">
																			<!--[if mso]><v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="'''+verification_link+'''" style="height:42px;width:261px;v-text-anchor:middle;" arcsize="10%" stroke="false" fillcolor="#00eb3b"><w:anchorlock/><v:textbox inset="0px,0px,0px,0px"><center style="color:#252626; font-family:Arial, sans-serif; font-size:16px"><![endif]--><a
																				href="'''+verification_link+'''"
																				style="text-decoration:none;display:inline-block;color:#252626;background-color:#00eb3b;border-radius:4px;width:auto;border-top:1px solid #00eb3b;border-right:1px solid #00eb3b;border-bottom:1px solid #00eb3b;border-left:1px solid #00eb3b;padding-top:5px;padding-bottom:5px;font-family:Arial, Helvetica Neue, Helvetica, sans-serif;text-align:center;mso-border-alt:none;word-break:keep-all;"
																				target="_blank"><span
																					style="padding-left:20px;padding-right:20px;font-size:16px;display:inline-block;letter-spacing:normal;"><span
																						style="font-size: 16px; line-height: 2; word-break: break-word; mso-line-height-alt: 32px;"><strong>VERIFY
																							MY EMAIL
																							ADDRESS</strong></span></span></a>
																			<!--[if mso]></center></v:textbox></v:roundrect><![endif]-->
																		</div>
																	</td>
																</tr>
															</table>
															<table border="0" cellpadding="0" cellspacing="0" class="text_block"
																role="presentation"
																style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
																width="100%">
																<tr>
																	<td
																		style="padding-top:20px;padding-right:45px;padding-bottom:45px;padding-left:45px;">
																		<div
																			style="font-family: 'Trebuchet MS', Tahoma, sans-serif">
																			<div
																				style="font-size: 14px; font-family: 'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif; mso-line-height-alt: 16.8px; color: #f0f5f9; line-height: 1.2;">
																				<p style="margin: 0; color: #ffffff;">If above button didn't
																					work, </p>
																				<p style="margin: 0;"><a
																						href="'''+verification_link+'''"
																						rel="noopener" style="color: #00eb3b;"
																						target="_blank">'''+verification_link+'''</a>
																				</p>
																				<p style="margin: 0; mso-line-height-alt: 16.8px;">
																					 </p>
																				<p style="margin: 0; color: #ffffff;">Best Regards,</p>
																				<p style="margin: 0;"><span
																						style="color:#ffffff;"><strong>Fodery |
																							Developer Team</strong></span></p>
																			</div>
																		</div>
																	</td>
																</tr>
															</table>
														</td>
													</tr>
												</tbody>
											</table>
										</td>
									</tr>
								</tbody>
							</table>
							<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-4"
								role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
								<tbody>
									<tr>
										<td>
											<table align="center" border="0" cellpadding="0" cellspacing="0"
												class="row-content stack" role="presentation"
												style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #1b1c1c; color: #000000; width: 605px;"
												width="605">
												<tbody>
													<tr>
														<td class="column"
															style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; padding-top: 5px; padding-bottom: 5px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;"
															width="100%">
															<div class="spacer_block"
																style="height:30px;line-height:30px;font-size:1px;"> </div>
														</td>
													</tr>
												</tbody>
											</table>
										</td>
									</tr>
								</tbody>
							</table>
							<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-5"
								role="presentation"
								style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #000000;" width="100%">
								<tbody>
									<tr>
										<td>
											<table align="center" border="0" cellpadding="0" cellspacing="0"
												class="row-content stack" role="presentation"
												style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #1b1c1c; color: #000000; width: 605px;"
												width="605">
												<tbody>
													<tr>
														<td class="column"
															style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; padding-top: 0px; padding-bottom: 10px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;"
															width="100%">
															<table border="0" cellpadding="0" cellspacing="0" class="html_block"
																role="presentation"
																style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
																width="100%">
																<tr>
																	<td>
																		<div align="center"
																			style="font-family:Arial, Helvetica Neue, Helvetica, sans-serif;text-align:center;">
																			<div style="height:30px;"> </div>
																		</div>
																	</td>
																</tr>
															</table>
															<table border="0" cellpadding="10" cellspacing="0"
																class="text_block" role="presentation"
																style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
																width="100%">
																<tr>
																	<td>
																		<div style="font-family: sans-serif">
																			<div
																				style="font-size: 12px; font-family: Arial, Helvetica Neue, Helvetica, sans-serif; mso-line-height-alt: 14.399999999999999px; color: #d6d6d6; line-height: 1.2;">
																				<p
																					style="margin: 0; font-size: 12px; text-align: center;">
																					<span style="">Follow us on social
																						media:</span></p>
																			</div>
																		</div>
																	</td>
																</tr>
															</table>
															<table border="0" cellpadding="0" cellspacing="0"
																class="social_block" role="presentation"
																style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
																width="100%">
																<tr>
																	<td
																		style="text-align:center;padding-right:0px;padding-left:0px;">
																		<table align="center" border="0" cellpadding="0"
																			cellspacing="0" class="social-table"
																			role="presentation"
																			style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"
																			width="126px">
																			<tr>
																				<td style="padding:0 5px 0 5px;"><a
																						href="https://www.facebook.com"
																						target="_blank"><img alt="Facebook"
																							height="32"
																							src="https://fod.suzanpradhan.com.np/media/facebook2x.png"
																							style="display: block; height: auto; border: 0;"
																							title="Facebook" width="32" /></a>
																				</td>
																				<td style="padding:0 5px 0 5px;"><a
																						href="https://twitter.com"
																						target="_blank"><img alt="Twitter"
																							height="32"
																							src="https://fod.suzanpradhan.com.np/media/twitter2x.png"
																							style="display: block; height: auto; border: 0;"
																							title="Twitter" width="32" /></a>
																				</td>
																				<td style="padding:0 5px 0 5px;"><a
																						href="https://www.instagram.com"
																						target="_blank"><img alt="Instagram"
																							height="32"
																							src="https://fod.suzanpradhan.com.np/media/instagram2x.png"
																							style="display: block; height: auto; border: 0;"
																							title="Instagram" width="32" /></a>
																				</td>
																			</tr>
																		</table>
																	</td>
																</tr>
															</table>
															<table border="0" cellpadding="25" cellspacing="0"
																class="text_block" role="presentation"
																style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"
																width="100%">
																<tr>
																	<td>
																		<div style="font-family: sans-serif">
																			<div
																				style="font-size: 12px; font-family: Arial, Helvetica Neue, Helvetica, sans-serif; mso-line-height-alt: 14.399999999999999px; color: #939799; line-height: 1.2;">
																				<p
																					style="margin: 0; text-align: center; mso-line-height-alt: 14.399999999999999px;">
																					 </p>
																				<p
																					style="margin: 0; text-align: center; mso-line-height-alt: 14.399999999999999px;">
																					 </p>
																				<p style="margin: 0; text-align: center;">
																					Copyright © 2021 Fodery Inc, All rights
																					reserved.</p>
																				<p
																					style="margin: 0; text-align: center; mso-line-height-alt: 14.399999999999999px;">
																					 </p>
																				<p style="margin: 0; text-align: center;">This
																					email was sent to you by Fodery. By
																					using our services, you agree to our <a
																						href="https://fod.suzanpradhan.com.np"
																						rel="noopener" style="color: #ffffff;"
																						target="_blank">Terms and
																						agreements</a>.</p>
																			</div>
																		</div>
																	</td>
																</tr>
															</table>
														</td>
													</tr>
												</tbody>
											</table>
										</td>
									</tr>
								</tbody>
							</table>
						</td>
					</tr>
				</tbody>
			</table><!-- End -->
		</body>

		</html>'''

	return verification_email
