cookie = """ogan_session_token	eqwo4p3loum6mddqnjea	eb.meituan.com	/	Session	39					Medium	
_dxuserid	G1rAdBWKwYVQRaQIOpZPKmE35zqa5qbbnvcYtGKDWE2qH1m3YMmFo-Xsz8ER0Dt2xp1BUNkvbhctco_AUCn_Hg	eb.meituan.com	/	Session	95					Medium	
ebbsid	G1rAdBWKwYVQRaQIOpZPKmE35zqa5qbbnvcYtGKDWE2qH1m3YMmFo-Xsz8ER0Dt2xp1BUNkvbhctco_AUCn_Hg	eb.meituan.com	/	Session	92					Medium	
_lxsdk_s	17af4f13c26-e8d-fe9-25f%7C%7C58	.meituan.com	/	2021-07-30T01:38:13.000Z	39					Medium	
e_u_id_3299326472	49d9033674ec32820fdea3ef727d9a75	.meituan.com	/	Session	49	✓	✓	None		Medium	
_lx_utm	utm_source%3DBaidu%26utm_medium%3Dorganic	.meituan.com	/	2021-08-03T02:00:47.000Z	48					Medium	
uuid	429f9d86e4343e66d5b2.1627351247.1.0.0	.meituan.com	/	2098-12-31T23:59:59.430Z	41	✓	✓	None		Medium	
_lxsdk	173e0b49834c8-060a40b66c27e5-3323765-295d29-173e0b49835c8	.meituan.com	/	2024-04-03T03:22:29.000Z	63					Medium	
_lxsdk_cuid	173e0b49834c8-060a40b66c27e5-3323765-295d29-173e0b49835c8	.meituan.com	/	2024-04-03T03:22:29.000Z	68					Medium	"""

for line in cookie.split("\n"):
	key = line.split()[0]
	value = line.split()[1]
	msg = '"{key}": "{value}",'.format(key=key, value=value)
	print(msg)