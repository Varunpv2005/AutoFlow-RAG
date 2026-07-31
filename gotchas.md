# Gotchas & Integration Quirks

## Embedding Dimension Mismatch Gotcha (2026-07-28)
- **Issue:** Changing embedding models (e.g. from 3072-dim Gemini embeddings to 384-dim Sentence Transformers `all-MiniLM-L6-v2`) causes `chromadb.errors.InvalidDimensionException: Embedding dimension 384 does not match collection dimensionality 3072`.
- **Fix:** Whenever the embedding model or dimension changes, clear/wipe the existing ChromaDB storage directory (`backend/app/data/chroma_db`) or collection so Chroma can initialize a fresh collection with the new dimensionality.

## Document Upload Quota Protection
- Document uploads now use **Sentence Transformers (`sentence-transformers/all-MiniLM-L6-v2`)** locally via `HuggingFaceEmbeddings`.
- Document parsing and embedding generation consume **zero Gemini API quota**.
- Gemini 2.5 Flash (`gemini-2.5-flash`) is used exclusively for final answer generation during chat.

## Google Gemini 2.5 Flash API Key Requirements
- Ensure `GEMINI_API_KEY` is set in `backend/.env`.
- Health check `/api/health` validates Gemini API connectivity for text generation.
[2026-07-28T19:56:31.450196] [init_db] Database initialized successfully.
[2026-07-28T19:56:42.358654] [Startup] Re-indexing 2 existing files into FAISS index...
[2026-07-28T20:10:57.362881] [DeleteFile] File 1 deleted successfully at 2026-07-28T20:10:57.362881
[2026-07-28T20:10:59.455163] [DeleteFile] File 2 deleted successfully at 2026-07-28T20:10:59.455163
[2026-07-28T21:20:57.929268] [init_db] Database initialized successfully.
[2026-07-28T21:21:18.588210] [init_db] Database initialized successfully.
[2026-07-28T21:21:37.282737] [init_db] Database initialized successfully.
[2026-07-28T21:24:02.108208] [init_db] Database initialized successfully.
[2026-07-28T21:26:50.136448] [init_db] Database initialized successfully.
[2026-07-28T21:27:09.050869] [init_db] Database initialized successfully.
[2026-07-28T21:27:26.045057] [init_db] Database initialized successfully.
[2026-07-28T21:27:42.657632] [init_db] Database initialized successfully.
[2026-07-28T21:28:03.830021] [init_db] Database initialized successfully.
[2026-07-28T21:30:37.066403] [init_db] Database initialized successfully.
[2026-07-28T21:31:23.477191] [DocIntel] Skipped doc intelligence due to error/quota limits: 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 20, model: gemini-2.5-flash\nPlease retry in 36.24586759s.', 'status': 'RESOURCE_EXHAUSTED', 'details': [{'@type': 'type.googleapis.com/google.rpc.Help', 'links': [{'description': 'Learn more about Gemini API quotas', 'url': 'https://ai.google.dev/gemini-api/docs/rate-limits'}]}, {'@type': 'type.googleapis.com/google.rpc.QuotaFailure', 'violations': [{'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_requests', 'quotaId': 'GenerateRequestsPerDayPerProjectPerModel-FreeTier', 'quotaDimensions': {'model': 'gemini-2.5-flash', 'location': 'global'}, 'quotaValue': '20'}]}, {'@type': 'type.googleapis.com/google.rpc.RetryInfo', 'retryDelay': '36s'}]}}
[2026-07-28T21:33:11.487083] [init_db] Database initialized successfully.
[2026-07-28T21:33:29.709120] [init_db] Database initialized successfully.
[2026-07-28T21:34:27.394091] [init_db] Database initialized successfully.
[2026-07-28T21:38:00.155182] [init_db] Database initialized successfully.
[2026-07-28T21:49:59.872703] [Chat] LLM inference failed: 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 20, model: gemini-2.5-flash\nPlease retry in 59.939524564s.', 'status': 'RESOURCE_EXHAUSTED', 'details': [{'@type': 'type.googleapis.com/google.rpc.Help', 'links': [{'description': 'Learn more about Gemini API quotas', 'url': 'https://ai.google.dev/gemini-api/docs/rate-limits'}]}, {'@type': 'type.googleapis.com/google.rpc.QuotaFailure', 'violations': [{'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_requests', 'quotaId': 'GenerateRequestsPerDayPerProjectPerModel-FreeTier', 'quotaDimensions': {'model': 'gemini-2.5-flash', 'location': 'global'}, 'quotaValue': '20'}]}, {'@type': 'type.googleapis.com/google.rpc.RetryInfo', 'retryDelay': '59s'}]}} at 2026-07-28T21:49:59.871698
[2026-07-28T22:12:14.835364] [Chat] LLM inference failed: 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 20, model: gemini-2.5-flash\nPlease retry in 44.201176607s.', 'status': 'RESOURCE_EXHAUSTED', 'details': [{'@type': 'type.googleapis.com/google.rpc.Help', 'links': [{'description': 'Learn more about Gemini API quotas', 'url': 'https://ai.google.dev/gemini-api/docs/rate-limits'}]}, {'@type': 'type.googleapis.com/google.rpc.QuotaFailure', 'violations': [{'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_requests', 'quotaId': 'GenerateRequestsPerDayPerProjectPerModel-FreeTier', 'quotaDimensions': {'location': 'global', 'model': 'gemini-2.5-flash'}, 'quotaValue': '20'}]}, {'@type': 'type.googleapis.com/google.rpc.RetryInfo', 'retryDelay': '44s'}]}} at 2026-07-28T22:12:14.835364
[2026-07-28T22:15:06.270987] [init_db] Database initialized successfully.
[2026-07-28T22:17:52.653944] [init_db] Database initialized successfully.
[2026-07-28T22:22:17.878075] [init_db] Database initialized successfully.
[2026-07-28T22:24:52.877870] [init_db] Database initialized successfully.
[2026-07-28T22:25:14.092771] [init_db] Database initialized successfully.
[2026-07-28T22:25:34.304036] [init_db] Database initialized successfully.
[2026-07-28T22:25:56.581318] [init_db] Database initialized successfully.
[2026-07-28T22:30:21.352721] [Chat] LLM inference failed: 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 20, model: gemini-2.5-flash\nPlease retry in 37.785241972s.', 'status': 'RESOURCE_EXHAUSTED', 'details': [{'@type': 'type.googleapis.com/google.rpc.Help', 'links': [{'description': 'Learn more about Gemini API quotas', 'url': 'https://ai.google.dev/gemini-api/docs/rate-limits'}]}, {'@type': 'type.googleapis.com/google.rpc.QuotaFailure', 'violations': [{'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_requests', 'quotaId': 'GenerateRequestsPerDayPerProjectPerModel-FreeTier', 'quotaDimensions': {'location': 'global', 'model': 'gemini-2.5-flash'}, 'quotaValue': '20'}]}, {'@type': 'type.googleapis.com/google.rpc.RetryInfo', 'retryDelay': '37s'}]}} at 2026-07-28T22:30:21.352721
[2026-07-28T22:30:21.357146] [Stream] Gemini quota: 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 20, model: gemini-2.5-flash\nPlease retry in 37.785241972s.', 'status': 'RESOURCE_EXHAUSTED', 'details': [{'@type': 'type.googleapis.com/google.rpc.Help', 'links': [{'description': 'Learn more about Gemini API quotas', 'url': 'https://ai.google.dev/gemini-api/docs/rate-limits'}]}, {'@type': 'type.googleapis.com/google.rpc.QuotaFailure', 'violations': [{'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_requests', 'quotaId': 'GenerateRequestsPerDayPerProjectPerModel-FreeTier', 'quotaDimensions': {'location': 'global', 'model': 'gemini-2.5-flash'}, 'quotaValue': '20'}]}, {'@type': 'type.googleapis.com/google.rpc.RetryInfo', 'retryDelay': '37s'}]}}
[2026-07-28T22:52:50.202909] [init_db] Database initialized successfully.
[2026-07-30T19:59:32.424447] [init_db] Database initialized successfully.
[2026-07-30T20:22:58.731449] event=contextual_event timestamp=2026-07-30T20:22:58.731449 message=boom request_id=req-3
[2026-07-30T20:23:45.904119] event=contextual_event timestamp=2026-07-30T20:23:45.904119 message=boom request_id=req-3
[2026-07-30T20:38:37.026882] event=[init_db] Database initialized successfully. timestamp=2026-07-30T20:38:37.026882 request_id=None
[2026-07-30T20:46:23.064645] event=[init_db] Database initialized successfully. timestamp=2026-07-30T20:46:23.064645 request_id=None
[2026-07-30T20:58:24.212578] event=request_completed timestamp=2026-07-30T20:58:24.212578 request_id=f3557f6c-68d4-4f25-a769-d7d751e3ef08 path=/api/health api_latency_ms=52.954 status_code=200
[2026-07-30T20:59:32.208348] event=http_exception timestamp=2026-07-30T20:59:32.208348 request_id=597a73b6-72c6-4cae-9a94-7768759e0a9d status_code=401 message=Invalid credentials path=/api/auth/login
[2026-07-30T20:59:32.209870] event=request_completed timestamp=2026-07-30T20:59:32.209870 request_id=597a73b6-72c6-4cae-9a94-7768759e0a9d path=/api/auth/login api_latency_ms=90.926 status_code=401
[2026-07-30T21:02:09.483710] event=request_completed timestamp=2026-07-30T21:02:09.483710 request_id=8d517ea2-09d6-4893-9a65-8e70cda2a06d path=/api/auth/signup api_latency_ms=323.118 status_code=200
[2026-07-30T21:02:25.355460] event=http_exception timestamp=2026-07-30T21:02:25.356922 request_id=bcea7a90-5a6b-4eb6-bcb5-6de23a7c5218 status_code=409 message=Username already exists path=/api/auth/signup
[2026-07-30T21:02:25.358546] event=request_completed timestamp=2026-07-30T21:02:25.358546 request_id=bcea7a90-5a6b-4eb6-bcb5-6de23a7c5218 path=/api/auth/signup api_latency_ms=6.094 status_code=409
[2026-07-30T21:03:13.497847] event=[init_db] Database initialized successfully. timestamp=2026-07-30T21:03:13.497847 request_id=None
[2026-07-30T21:03:39.375064] event=[init_db] Database initialized successfully. timestamp=2026-07-30T21:03:39.376062 request_id=None
[2026-07-30T21:03:54.214455] event=request_completed timestamp=2026-07-30T21:03:54.214455 request_id=9e0367da-5dcc-4831-8a33-bd9b9896b8be path=/api/health api_latency_ms=4.518 status_code=200
[2026-07-30T21:04:05.052348] event=request_completed timestamp=2026-07-30T21:04:05.052348 request_id=74b16a22-0780-4dec-be41-cb0b2fe90837 path=/api/auth/signup api_latency_ms=284.999 status_code=200
[2026-07-30T21:04:17.201241] event=request_completed timestamp=2026-07-30T21:04:17.201241 request_id=15052c20-04a3-431d-bc16-f936c7d5256c path=/api/auth/login api_latency_ms=279.34 status_code=200
[2026-07-30T21:05:54.485310] event=[init_db] Database initialized successfully. timestamp=2026-07-30T21:05:54.485310 request_id=None
[2026-07-30T21:07:01.453530] event=request_completed timestamp=2026-07-30T21:07:01.453530 request_id=75b8684e-c54b-476a-928a-530c2faf56fe path=/api/auth/signup api_latency_ms=288.521 status_code=200
[2026-07-30T21:07:01.531859] event=request_completed timestamp=2026-07-30T21:07:01.531859 request_id=2c9cd304-8c78-4c28-9c2a-84ff6ab5520f path=/api/health api_latency_ms=9.291 status_code=200
[2026-07-30T21:07:01.540885] event=request_completed timestamp=2026-07-30T21:07:01.540885 request_id=724d20ef-785d-4768-8001-3331b85c1d1a path=/api/files api_latency_ms=21.854 status_code=200
[2026-07-30T21:07:01.546494] event=request_completed timestamp=2026-07-30T21:07:01.546494 request_id=0d4c1ad3-ff39-4560-a1e1-71abceaf72fd path=/api/chat/history api_latency_ms=18.932 status_code=200
[2026-07-30T21:07:01.551002] event=request_completed timestamp=2026-07-30T21:07:01.551002 request_id=90ad0d88-b6bb-4ba5-b5fc-462b6381e460 path=/api/health api_latency_ms=6.521 status_code=200
[2026-07-30T21:07:01.563167] event=request_completed timestamp=2026-07-30T21:07:01.563167 request_id=83da52f2-4975-4bf0-8d62-c71016169c8b path=/api/files api_latency_ms=10.146 status_code=200
[2026-07-30T21:07:01.566169] event=request_completed timestamp=2026-07-30T21:07:01.566169 request_id=ea73b3e2-cd1c-41e4-88cc-4e64f0b52641 path=/api/chat/history api_latency_ms=8.157 status_code=200
[2026-07-30T21:08:54.180328] event=request_completed timestamp=2026-07-30T21:08:54.180328 request_id=7b54a4ee-25a6-4e28-b7e8-8610f6f2594b path=/api/upload api_latency_ms=4196.704 status_code=200
[2026-07-30T21:08:54.247303] event=request_completed timestamp=2026-07-30T21:08:54.247303 request_id=9415c3b4-e9db-4d02-805e-56860dd2880f path=/api/analytics api_latency_ms=14.179 status_code=200
[2026-07-30T21:14:51.311041] event=request_completed timestamp=2026-07-30T21:14:51.311041 request_id=68675cfd-0cf2-4f9e-8a36-3e50e7c17663 path=/api/health api_latency_ms=21.533 status_code=200
[2026-07-30T21:14:51.326207] event=request_completed timestamp=2026-07-30T21:14:51.326207 request_id=0ad4168a-a02e-4ed3-aca0-a18ea22de093 path=/api/files api_latency_ms=40.328 status_code=200
[2026-07-30T21:14:51.331728] event=request_completed timestamp=2026-07-30T21:14:51.331728 request_id=7dbf180f-7da7-4fd1-9843-fbe4327fb6cb path=/api/health api_latency_ms=6.519 status_code=200
[2026-07-30T21:14:51.471233] event=request_completed timestamp=2026-07-30T21:14:51.471233 request_id=dee1e44e-05b7-4a81-bf5f-1b241492a156 path=/api/analytics api_latency_ms=16.4 status_code=200
[2026-07-30T21:15:09.201380] event=request_completed timestamp=2026-07-30T21:15:09.201380 request_id=ce777c8c-f1b7-4006-9ba6-a15273d06708 path=/api/files api_latency_ms=9.067 status_code=200
[2026-07-30T21:15:09.265688] event=request_completed timestamp=2026-07-30T21:15:09.266703 request_id=def09629-309b-467a-8289-e2488d71d582 path=/api/analytics api_latency_ms=7.684 status_code=200
[2026-07-30T21:15:19.208601] event=request_completed timestamp=2026-07-30T21:15:19.208601 request_id=358853ad-6703-4ac2-930b-12a02214a9bd path=/api/chat/history api_latency_ms=7.533 status_code=200
[2026-07-30T21:15:19.223847] event=request_completed timestamp=2026-07-30T21:15:19.223847 request_id=57d50ea6-b3b0-4e58-872e-2879781ca37c path=/api/chat/history api_latency_ms=6.062 status_code=200
[2026-07-30T21:15:20.183262] event=request_completed timestamp=2026-07-30T21:15:20.183262 request_id=2ab3753a-316b-41cd-905d-f4e75fe3d248 path=/api/chat/history api_latency_ms=7.547 status_code=200
[2026-07-30T21:16:33.925389] event=[init_db] Database initialized successfully. timestamp=2026-07-30T21:16:33.926895 request_id=None
[2026-07-30T21:19:04.388464] event=request_completed timestamp=2026-07-30T21:19:04.388464 request_id=5ff122e7-6511-4578-9d65-677f1dd8085d path=/api/health api_latency_ms=24.655 status_code=200
[2026-07-30T21:19:04.404826] event=request_completed timestamp=2026-07-30T21:19:04.404826 request_id=95f434e2-bc87-4d7a-a617-d5ee213a6e49 path=/api/health api_latency_ms=3.511 status_code=200
[2026-07-30T21:19:04.406839] event=request_completed timestamp=2026-07-30T21:19:04.406839 request_id=a63976de-acd1-4d09-ae85-bf2b3f6b8990 path=/api/files api_latency_ms=43.532 status_code=200
[2026-07-30T21:19:04.416537] event=request_completed timestamp=2026-07-30T21:19:04.416537 request_id=f8f87c91-69ec-4837-b7ca-85b1fd61a6f7 path=/api/chat/history api_latency_ms=52.728 status_code=200
[2026-07-30T21:19:04.422546] event=request_completed timestamp=2026-07-30T21:19:04.422546 request_id=de50221d-7713-451b-b87e-ee6ccc1cbb17 path=/api/files api_latency_ms=7.522 status_code=200
[2026-07-30T21:19:04.434262] event=request_completed timestamp=2026-07-30T21:19:04.434262 request_id=e779dbc3-81f3-4f92-9637-18e9ce310b2f path=/api/chat/history api_latency_ms=6.192 status_code=200
[2026-07-30T21:20:13.452430] event=[Chat] LLM inference failed: 503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}} at 2026-07-30T21:20:13.452430 timestamp=2026-07-30T21:20:13.452430 request_id=a174959f-1ebc-405a-9074-8acc872cb622
[2026-07-30T21:20:13.453476] event=[Chat] Unexpected error: 503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}} timestamp=2026-07-30T21:20:13.453476 request_id=a174959f-1ebc-405a-9074-8acc872cb622
[2026-07-30T21:20:13.455475] event=request_error timestamp=2026-07-30T21:20:13.455475 request_id=a174959f-1ebc-405a-9074-8acc872cb622 path=/api/chat api_latency_ms=2599.421 error=503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}}
[2026-07-30T21:20:13.456474] event=generic_exception timestamp=2026-07-30T21:20:13.456474 request_id=a174959f-1ebc-405a-9074-8acc872cb622 error=503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}} path=/api/chat
[2026-07-30T22:46:26.826661] event=[init_db] Database initialized successfully. timestamp=2026-07-30T22:46:26.826661 request_id=None
[2026-07-30T22:46:53.258096] event=[Chat] Gemini service unavailable: Gemini service is temporarily unavailable timestamp=2026-07-30T22:46:53.259139 request_id=e8de7274-cc14-488e-9fe4-0da70a231cd5
[2026-07-30T22:46:53.259686] event=request_completed timestamp=2026-07-30T22:46:53.259686 request_id=e8de7274-cc14-488e-9fe4-0da70a231cd5 path=/api/chat api_latency_ms=7.264 status_code=503
[2026-07-30T22:49:34.844010] event=[init_db] Database initialized successfully. timestamp=2026-07-30T22:49:34.844010 request_id=None
[2026-07-30T22:51:14.153271] event=request_completed timestamp=2026-07-30T22:51:14.153271 request_id=571b2c3e-3efe-45a7-9d76-7470f20e7dc3 path=/api/health api_latency_ms=8.832 status_code=200
[2026-07-30T22:51:14.225982] event=request_completed timestamp=2026-07-30T22:51:14.225982 request_id=2cc278de-e82f-4778-96ea-107ab1e8ab24 path=/api/health api_latency_ms=21.729 status_code=200
[2026-07-30T22:51:14.230089] event=request_completed timestamp=2026-07-30T22:51:14.230089 request_id=5fa7913b-f8c8-44fe-aee0-5d3786433478 path=/api/files api_latency_ms=83.617 status_code=200
[2026-07-30T22:51:14.233321] event=request_completed timestamp=2026-07-30T22:51:14.233321 request_id=ec429fcb-0fe7-4b3a-b7c9-8a87f15a8ff8 path=/api/chat/history api_latency_ms=85.871 status_code=200
[2026-07-30T22:51:14.259245] event=request_completed timestamp=2026-07-30T22:51:14.259245 request_id=d58f8e55-7f88-43fb-9df9-a82ab6a80445 path=/api/files api_latency_ms=17.969 status_code=200
[2026-07-30T22:51:14.261844] event=request_completed timestamp=2026-07-30T22:51:14.261844 request_id=92ffa880-adc3-43e4-97a2-ae64ad99d2bc path=/api/chat/history api_latency_ms=14.783 status_code=200
[2026-07-30T22:51:21.645712] event=chat_completed timestamp=2026-07-30T22:51:21.645712 retrieval_latency_ms=0.338 llm_latency_ms=3.34 chunk_count=1 user_id=3 request_id=b560f3f2-544a-439b-aa7e-9061022bc076
[2026-07-30T22:51:21.676793] event=request_completed timestamp=2026-07-30T22:51:21.676793 request_id=b560f3f2-544a-439b-aa7e-9061022bc076 path=/api/chat api_latency_ms=3715.614 status_code=200
[2026-07-30T22:54:16.769699] event=[init_db] Database initialized successfully. timestamp=2026-07-30T22:54:16.769699 request_id=None
[2026-07-30T22:54:48.900979] event=[init_db] Database initialized successfully. timestamp=2026-07-30T22:54:48.900979 request_id=None
[2026-07-30T22:57:33.191597] event=[init_db] Database initialized successfully. timestamp=2026-07-30T22:57:33.191597 request_id=None
[2026-07-30T22:57:59.442812] event=[init_db] Database initialized successfully. timestamp=2026-07-30T22:57:59.443799 request_id=None
[2026-07-30T23:03:31.265424] event=request_completed timestamp=2026-07-30T23:03:31.265424 request_id=9079a307-0b00-421b-9ba2-6141e8fe4710 path=/api/chat/history api_latency_ms=43.476 status_code=200
[2026-07-30T23:03:31.284003] event=request_completed timestamp=2026-07-30T23:03:31.284003 request_id=a6d59f98-5efa-4f8a-bc44-929ed63ebe63 path=/api/chat/history api_latency_ms=6.517 status_code=200
[2026-07-30T23:03:33.164456] event=request_completed timestamp=2026-07-30T23:03:33.164456 request_id=4be44471-1074-4764-bb5f-c3d2607aed87 path=/api/chat/history api_latency_ms=7.167 status_code=200
[2026-07-30T23:04:54.994863] event=[init_db] Database initialized successfully. timestamp=2026-07-30T23:04:54.994863 request_id=None
[2026-07-30T23:05:23.706101] event=[init_db] Database initialized successfully. timestamp=2026-07-30T23:05:23.706101 request_id=None
[2026-07-30T23:08:32.440061] event=[init_db] Database initialized successfully. timestamp=2026-07-30T23:08:32.440061 request_id=None
[2026-07-30T23:08:53.931341] event=[init_db] Database initialized successfully. timestamp=2026-07-30T23:08:53.931341 request_id=None
[2026-07-30T23:10:08.374587] event=[init_db] Database initialized successfully. timestamp=2026-07-30T23:10:08.375587 request_id=None
[2026-07-30T23:11:34.686107] event=[init_db] Database initialized successfully. timestamp=2026-07-30T23:11:34.686107 request_id=None
[2026-07-30T23:11:57.974044] event=[init_db] Database initialized successfully. timestamp=2026-07-30T23:11:57.974044 request_id=None
[2026-07-30T23:12:24.616055] event=[init_db] Database initialized successfully. timestamp=2026-07-30T23:12:24.616055 request_id=None
[2026-07-30T23:12:47.526921] event=[init_db] Database initialized successfully. timestamp=2026-07-30T23:12:47.527920 request_id=None
[2026-07-30T23:16:05.293786] event=[init_db] Database initialized successfully. timestamp=2026-07-30T23:16:05.293786 request_id=None
[2026-07-30T23:16:09.959416] event=[init_db] Database initialized successfully. timestamp=2026-07-30T23:16:09.959416 request_id=None
[2026-07-30T23:16:28.962960] event=[init_db] Database initialized successfully. timestamp=2026-07-30T23:16:28.962960 request_id=None
[2026-07-30T23:20:12.963713] event=[init_db] Database initialized successfully. timestamp=2026-07-30T23:20:12.963713 request_id=None
[2026-07-30T23:24:09.980795] event=[init_db] Database initialized successfully. timestamp=2026-07-30T23:24:09.980795 request_id=None
[2026-07-30T23:27:11.175407] event=request_completed timestamp=2026-07-30T23:27:11.176417 request_id=a80ce340-6f2c-4de2-ab83-823b2c06fcb6 path=/api/health api_latency_ms=32.828 status_code=200
[2026-07-30T23:30:19.953982] event=http_exception timestamp=2026-07-30T23:30:19.953982 request_id=f871ab63-a329-49ac-a0d3-52e8cf8e3313 status_code=401 message=Invalid credentials path=/api/auth/login
[2026-07-30T23:30:19.957569] event=request_completed timestamp=2026-07-30T23:30:19.957569 request_id=f871ab63-a329-49ac-a0d3-52e8cf8e3313 path=/api/auth/login api_latency_ms=70.421 status_code=401
[2026-07-30T23:30:40.683523] event=request_completed timestamp=2026-07-30T23:30:40.683523 request_id=2156b29d-b829-4021-b079-db25e9eea7b5 path=/api/auth/signup api_latency_ms=429.309 status_code=200
[2026-07-30T23:30:40.872273] event=request_completed timestamp=2026-07-30T23:30:40.872273 request_id=9fbe213c-0663-4b1f-af93-035702fbee28 path=/api/health api_latency_ms=13.178 status_code=200
[2026-07-30T23:30:40.886428] event=request_completed timestamp=2026-07-30T23:30:40.886428 request_id=2ff5808d-6fe3-4b81-86ff-6f122825f586 path=/api/files api_latency_ms=37.73 status_code=200
[2026-07-30T23:30:40.894474] event=request_completed timestamp=2026-07-30T23:30:40.894474 request_id=7327affe-ebb5-4d83-a0f8-3b3f0c61ebb0 path=/api/chat/history api_latency_ms=36.382 status_code=200
[2026-07-30T23:30:40.898206] event=request_completed timestamp=2026-07-30T23:30:40.898206 request_id=761d7f7e-0afe-48dd-a447-2b8952535989 path=/api/health api_latency_ms=6.744 status_code=200
[2026-07-30T23:30:40.913911] event=request_completed timestamp=2026-07-30T23:30:40.913911 request_id=96958a92-2482-46ab-9ffc-55fd9f8ecb3b path=/api/files api_latency_ms=10.184 status_code=200
[2026-07-30T23:30:40.924537] event=request_completed timestamp=2026-07-30T23:30:40.924537 request_id=7d38f837-f39e-489d-8520-1e6394ca792e path=/api/chat/history api_latency_ms=13.347 status_code=200
[2026-07-30T23:31:16.588986] event=request_completed timestamp=2026-07-30T23:31:16.588986 request_id=96e718fa-10b3-4ae2-b0a4-db46405ed74f path=/api/upload api_latency_ms=5093.461 status_code=200
[2026-07-30T23:33:08.375366] event=request_completed timestamp=2026-07-30T23:33:08.375366 request_id=d561bd05-3b85-4b12-aff0-10290d5bda42 path=/api/chat/stream api_latency_ms=29.671 status_code=200
[2026-07-30T23:33:11.370870] event=chat_completed timestamp=2026-07-30T23:33:11.370870 retrieval_latency_ms=0.089 llm_latency_ms=2.91 chunk_count=1 user_id=4 request_id=None
[2026-07-30T23:33:28.166947] event=request_completed timestamp=2026-07-30T23:33:28.166947 request_id=6786bf8b-664a-4047-b889-9637f87d7a25 path=/api/auth/login api_latency_ms=437.418 status_code=200
[2026-07-30T23:33:28.288287] event=request_completed timestamp=2026-07-30T23:33:28.288287 request_id=70d2249a-022c-4e06-95c2-f6e334cf4954 path=/api/chat/history api_latency_ms=14.071 status_code=200
[2026-07-30T23:35:23.420089] event=request_completed timestamp=2026-07-30T23:35:23.420089 request_id=e7462e98-2548-4cc3-a3e0-5e468fc6c833 path=/api/health api_latency_ms=42.548 status_code=200
[2026-07-30T23:35:23.455475] event=request_completed timestamp=2026-07-30T23:35:23.456101 request_id=bcac8f20-2115-4d36-ba9e-a67e44e9d199 path=/api/chat/history api_latency_ms=77.934 status_code=200
[2026-07-30T23:35:23.465113] event=request_completed timestamp=2026-07-30T23:35:23.465113 request_id=0fbfa782-2b48-44ad-a8e6-7f20f93b6755 path=/api/files api_latency_ms=95.85 status_code=200
[2026-07-30T23:35:23.469589] event=request_completed timestamp=2026-07-30T23:35:23.469589 request_id=18684eef-c31e-4d46-98ad-78ec2840fcc8 path=/api/health api_latency_ms=29.061 status_code=200
[2026-07-30T23:35:23.506249] event=request_completed timestamp=2026-07-30T23:35:23.506249 request_id=5853ccf3-00cb-4a33-a5eb-d782f3caf0ef path=/api/chat/history api_latency_ms=26.573 status_code=200
[2026-07-30T23:35:23.515692] event=request_completed timestamp=2026-07-30T23:35:23.515692 request_id=4b97eab5-4eca-4f61-9027-b1c8d4ad472b path=/api/files api_latency_ms=24.796 status_code=200
[2026-07-30T23:35:28.194321] event=request_completed timestamp=2026-07-30T23:35:28.194321 request_id=0a11efba-16b2-46dc-8621-64748a3f2952 path=/api/analytics api_latency_ms=77.547 status_code=200
[2026-07-30T23:35:48.521740] event=request_completed timestamp=2026-07-30T23:35:48.522748 request_id=3f34d2c7-f984-442f-a10f-581dae11874a path=/api/analytics api_latency_ms=37.23 status_code=200
[2026-07-31T14:14:41.353262] event=[init_db] Database initialized successfully. timestamp=2026-07-31T14:14:41.353262 request_id=None
[2026-07-31T14:15:09.637794] event=chat_completed timestamp=2026-07-31T14:15:09.637794 retrieval_latency_ms=0.0 llm_latency_ms=0.0 chunk_count=1 user_id=1 request_id=None
[2026-07-31T14:15:12.708655] event=[Chat] Gemini service unavailable: Gemini service is temporarily unavailable timestamp=2026-07-31T14:15:12.708655 request_id=13e0ca31-80ed-4137-b14c-1ddd6059d041
[2026-07-31T14:15:12.711914] event=request_completed timestamp=2026-07-31T14:15:12.711914 request_id=13e0ca31-80ed-4137-b14c-1ddd6059d041 path=/api/chat api_latency_ms=14.202 status_code=503
[2026-07-31T14:15:12.731980] event=contextual_event timestamp=2026-07-31T14:15:12.731980 message=boom request_id=req-3
[2026-07-31T14:17:24.936148] event=[init_db] Database initialized successfully. timestamp=2026-07-31T14:17:24.936148 request_id=None
[2026-07-31T14:17:33.637643] event=chat_completed timestamp=2026-07-31T14:17:33.637643 retrieval_latency_ms=0.0 llm_latency_ms=0.0 chunk_count=1 user_id=1 request_id=None
[2026-07-31T14:17:35.087020] event=[Chat] Gemini service unavailable: Gemini service is temporarily unavailable timestamp=2026-07-31T14:17:35.087020 request_id=40b2f385-2968-4800-ae4a-ef8be8524232
[2026-07-31T14:17:35.088526] event=request_completed timestamp=2026-07-31T14:17:35.088526 request_id=40b2f385-2968-4800-ae4a-ef8be8524232 path=/api/chat api_latency_ms=5.537 status_code=503
[2026-07-31T14:17:35.097684] event=contextual_event timestamp=2026-07-31T14:17:35.097684 message=boom request_id=req-3
[2026-07-31T14:19:40.828135] event=[init_db] Database initialized successfully. timestamp=2026-07-31T14:19:40.828135 request_id=None
[2026-07-31T14:19:49.577163] event=chat_completed timestamp=2026-07-31T14:19:49.577163 retrieval_latency_ms=0.0 llm_latency_ms=0.0 chunk_count=1 user_id=1 request_id=None
[2026-07-31T14:19:51.420356] event=[Chat] Gemini service unavailable: Gemini service is temporarily unavailable timestamp=2026-07-31T14:19:51.420356 request_id=b6bb7ad4-b504-4113-9e13-957f47d5bf73
[2026-07-31T14:19:51.421351] event=request_completed timestamp=2026-07-31T14:19:51.421351 request_id=b6bb7ad4-b504-4113-9e13-957f47d5bf73 path=/api/chat api_latency_ms=6.04 status_code=503
[2026-07-31T14:19:51.429585] event=contextual_event timestamp=2026-07-31T14:19:51.429585 message=boom request_id=req-3
[2026-07-31T15:14:46.187143] event=[init_db] Database initialized successfully. timestamp=2026-07-31T15:14:46.187143 request_id=None
[2026-07-31T15:14:58.048345] event=chat_completed timestamp=2026-07-31T15:14:58.048345 retrieval_latency_ms=0.0 llm_latency_ms=0.0 chunk_count=1 user_id=1 request_id=None
[2026-07-31T15:14:59.459463] event=[Chat] Gemini service unavailable: Gemini service is temporarily unavailable timestamp=2026-07-31T15:14:59.459463 request_id=b5e12cf1-51e1-4761-8b91-85b9a22caf92
[2026-07-31T15:14:59.460995] event=request_completed timestamp=2026-07-31T15:14:59.460995 request_id=b5e12cf1-51e1-4761-8b91-85b9a22caf92 path=/api/chat api_latency_ms=6.529 status_code=503
[2026-07-31T15:14:59.469637] event=contextual_event timestamp=2026-07-31T15:14:59.469637 message=boom request_id=req-3
[2026-07-31T15:22:58.390168] event=[init_db] Database initialized successfully. timestamp=2026-07-31T15:22:58.390168 request_id=None
[2026-07-31T15:23:31.116211] event=[init_db] Database initialized successfully. timestamp=2026-07-31T15:23:31.116211 request_id=None
[2026-07-31T15:23:47.528957] event=[init_db] Database initialized successfully. timestamp=2026-07-31T15:23:47.528957 request_id=None
[2026-07-31T15:25:19.248656] event=http_exception timestamp=2026-07-31T15:25:19.248656 request_id=44939db6-6e0a-452d-94b5-5cfcc61e6805 status_code=401 message=Invalid credentials path=/api/auth/login
[2026-07-31T15:25:19.249657] event=request_completed timestamp=2026-07-31T15:25:19.249657 request_id=44939db6-6e0a-452d-94b5-5cfcc61e6805 path=/api/auth/login api_latency_ms=12.594 status_code=401
[2026-07-31T15:25:26.760643] event=request_completed timestamp=2026-07-31T15:25:26.760643 request_id=e72e1243-ae25-4d05-b20e-c206eef6235e path=/api/auth/signup api_latency_ms=280.804 status_code=200
[2026-07-31T15:25:26.873457] event=request_completed timestamp=2026-07-31T15:25:26.873457 request_id=4ce5e73c-cabd-4683-bf13-0e721a0127f0 path=/api/health api_latency_ms=7.942 status_code=200
[2026-07-31T15:25:26.886478] event=request_completed timestamp=2026-07-31T15:25:26.886478 request_id=914fe0cd-f502-42b2-80a1-2b9cfa34a780 path=/api/files api_latency_ms=21.47 status_code=200
[2026-07-31T15:25:26.887482] event=request_completed timestamp=2026-07-31T15:25:26.887482 request_id=c61c2123-2080-40f6-9fac-8849f043c43f path=/api/health api_latency_ms=3.003 status_code=200
[2026-07-31T15:25:26.891019] event=request_completed timestamp=2026-07-31T15:25:26.891019 request_id=6d45e80c-c130-4259-af2c-0197d48deb2b path=/api/chat/history api_latency_ms=24.944 status_code=200
[2026-07-31T15:25:26.906715] event=request_completed timestamp=2026-07-31T15:25:26.906715 request_id=d56208ce-b74f-4ed7-96b7-5139a8228fd2 path=/api/files api_latency_ms=7.524 status_code=200
[2026-07-31T15:25:26.908715] event=request_completed timestamp=2026-07-31T15:25:26.908715 request_id=727d3781-126a-4fc9-a345-836219ae4dd4 path=/api/chat/history api_latency_ms=7.517 status_code=200
[2026-07-31T15:26:27.806947] event=request_completed timestamp=2026-07-31T15:26:27.806947 request_id=24f4a121-9a15-410f-b5e9-749afe351e0f path=/api/upload api_latency_ms=6217.904 status_code=200
[2026-07-31T15:26:32.907123] event=request_completed timestamp=2026-07-31T15:26:32.907123 request_id=f907cd96-fbee-49f7-81a7-16c6d875d4da path=/api/chat/stream api_latency_ms=6.052 status_code=200
[2026-07-31T15:26:35.575979] event=chat_completed timestamp=2026-07-31T15:26:35.575979 retrieval_latency_ms=0.026 llm_latency_ms=2.64 chunk_count=1 user_id=5 request_id=None
[2026-07-31T16:01:01.590630] event=[init_db] Database initialized successfully. timestamp=2026-07-31T16:01:01.592136 request_id=None
[2026-07-31T16:01:13.882665] event=chat_completed timestamp=2026-07-31T16:01:13.882665 retrieval_latency_ms=0.0 llm_latency_ms=0.0 chunk_count=1 user_id=1 request_id=None
[2026-07-31T16:01:15.382151] event=[Chat] Gemini service unavailable: Gemini service is temporarily unavailable timestamp=2026-07-31T16:01:15.382151 request_id=005864aa-248f-4fa0-9a67-1e68f16e4597
[2026-07-31T16:01:15.383150] event=request_completed timestamp=2026-07-31T16:01:15.383150 request_id=005864aa-248f-4fa0-9a67-1e68f16e4597 path=/api/chat api_latency_ms=6.606 status_code=503
[2026-07-31T16:01:15.394313] event=contextual_event timestamp=2026-07-31T16:01:15.394313 message=boom request_id=req-3
[2026-07-31T16:02:49.982934] event=request_completed timestamp=2026-07-31T16:02:49.983949 request_id=97175065-5d99-4ecf-9e96-9c2f8f32a773 path=/api/health api_latency_ms=223.222 status_code=200
[2026-07-31T16:02:50.030367] event=request_completed timestamp=2026-07-31T16:02:50.030367 request_id=898246e4-cb30-4393-9aec-3fa40ae6ac36 path=/api/chat/history api_latency_ms=271.656 status_code=200
[2026-07-31T16:02:50.033975] event=request_completed timestamp=2026-07-31T16:02:50.033975 request_id=deee6033-d221-4d41-a024-42117f0ff48a path=/api/health api_latency_ms=18.396 status_code=200
[2026-07-31T16:02:50.036990] event=request_completed timestamp=2026-07-31T16:02:50.036990 request_id=69e96e69-6e5a-4009-9392-01f154b78717 path=/api/files api_latency_ms=282.008 status_code=200
[2026-07-31T16:02:50.053414] event=request_completed timestamp=2026-07-31T16:02:50.053414 request_id=175a837e-5e9a-46f0-93e1-b065c4e04cbe path=/api/chat/history api_latency_ms=10.857 status_code=200
[2026-07-31T16:02:50.057402] event=request_completed timestamp=2026-07-31T16:02:50.058439 request_id=44e618bd-e61f-4b2f-bb52-423a680f6555 path=/api/files api_latency_ms=8.224 status_code=200
[2026-07-31T16:03:03.314422] event=request_completed timestamp=2026-07-31T16:03:03.314422 request_id=2ffa256d-7f56-4992-93c4-441dd8bd4c9f path=/api/chat/stream api_latency_ms=24.74 status_code=200
[2026-07-31T16:03:05.791343] event=chat_completed timestamp=2026-07-31T16:03:05.791343 retrieval_latency_ms=0.272 llm_latency_ms=2.2 chunk_count=2 user_id=5 request_id=None
[2026-07-31T16:08:45.261965] event=request_completed timestamp=2026-07-31T16:08:45.261965 request_id=542070a3-8754-4efa-8329-31ff9d7edfaf path=/api/upload api_latency_ms=15876.377 status_code=200
[2026-07-31T16:08:56.547118] event=[DeleteFile] File 3 deleted successfully at 2026-07-31T16:08:56.547118 timestamp=2026-07-31T16:08:56.547118 request_id=b90669c8-6983-4466-a23c-c5c8df9bf781
[2026-07-31T16:09:01.342566] event=request_completed timestamp=2026-07-31T16:09:01.342566 request_id=b90669c8-6983-4466-a23c-c5c8df9bf781 path=/api/files/3 api_latency_ms=4831.741 status_code=200
[2026-07-31T16:09:32.498302] event=request_completed timestamp=2026-07-31T16:09:32.498302 request_id=99e91457-22e2-4805-a2e7-a4f67f68dbd0 path=/api/chat/stream api_latency_ms=5.002 status_code=200
[2026-07-31T16:09:36.351566] event=chat_completed timestamp=2026-07-31T16:09:36.351566 retrieval_latency_ms=0.057 llm_latency_ms=3.8 chunk_count=4 user_id=5 request_id=None
[2026-07-31T16:09:52.561243] event=request_completed timestamp=2026-07-31T16:09:52.561243 request_id=92806169-1c42-4ef1-b85d-eac8a5a47e91 path=/api/chat/stream api_latency_ms=5.686 status_code=200
[2026-07-31T16:09:55.079329] event=chat_completed timestamp=2026-07-31T16:09:55.079329 retrieval_latency_ms=0.018 llm_latency_ms=2.5 chunk_count=4 user_id=5 request_id=None
[2026-07-31T16:10:25.770221] event=request_completed timestamp=2026-07-31T16:10:25.770221 request_id=ada9db08-66d7-4155-9211-6e2fda4405d3 path=/api/chat/stream api_latency_ms=4.955 status_code=200
[2026-07-31T16:10:27.739729] event=chat_completed timestamp=2026-07-31T16:10:27.739729 retrieval_latency_ms=0.015 llm_latency_ms=1.95 chunk_count=3 user_id=5 request_id=None
[2026-07-31T16:11:25.422248] event=request_error timestamp=2026-07-31T16:11:25.422248 request_id=8f2ba62c-3f06-4dd1-bd64-27923f2a8af3 path=/api/analytics api_latency_ms=19.604 error=name 'analytics' is not defined
[2026-07-31T16:11:25.424249] event=generic_exception timestamp=2026-07-31T16:11:25.424249 request_id=8f2ba62c-3f06-4dd1-bd64-27923f2a8af3 error=name 'analytics' is not defined path=/api/analytics
[2026-07-31T16:16:58.674202] event=[init_db] Database initialized successfully. timestamp=2026-07-31T16:16:58.674202 request_id=None
[2026-07-31T16:18:36.732351] event=[init_db] Database initialized successfully. timestamp=2026-07-31T16:18:36.732351 request_id=None
[2026-07-31T16:19:11.612752] event=[init_db] Database initialized successfully. timestamp=2026-07-31T16:19:11.612752 request_id=None
[2026-07-31T16:19:24.457734] event=chat_completed timestamp=2026-07-31T16:19:24.457734 retrieval_latency_ms=0.0 llm_latency_ms=0.0 chunk_count=1 user_id=1 request_id=None
[2026-07-31T16:19:26.586818] event=[Chat] Gemini service unavailable: Gemini service is temporarily unavailable timestamp=2026-07-31T16:19:26.586818 request_id=7cebfb42-cbb1-492a-bbf0-50de593a4c6e
[2026-07-31T16:19:26.588818] event=request_completed timestamp=2026-07-31T16:19:26.588818 request_id=7cebfb42-cbb1-492a-bbf0-50de593a4c6e path=/api/chat api_latency_ms=8.523 status_code=503
[2026-07-31T16:19:26.602615] event=contextual_event timestamp=2026-07-31T16:19:26.602615 message=boom request_id=req-3
[2026-07-31T16:24:05.804577] event=[init_db] Database initialized successfully. timestamp=2026-07-31T16:24:05.804577 request_id=None
[2026-07-31T16:24:28.050568] event=request_completed timestamp=2026-07-31T16:24:28.050568 request_id=739e989e-11f8-46dd-bd31-08e37f168eae path=/api/auth/login api_latency_ms=368.123 status_code=200
[2026-07-31T16:24:28.091588] event=request_completed timestamp=2026-07-31T16:24:28.091588 request_id=dc62ca52-db1d-4ba9-ba4b-50afd02735f8 path=/api/analytics api_latency_ms=31.456 status_code=200
[2026-07-31T16:28:04.352105] event=request_completed timestamp=2026-07-31T16:28:04.352105 request_id=d8bcb85e-a652-4155-99a2-c2ae364fd944 path=/api/health api_latency_ms=20.592 status_code=200
[2026-07-31T16:28:04.382007] event=request_completed timestamp=2026-07-31T16:28:04.382007 request_id=60d35185-60c0-4b47-9783-26767adc37c1 path=/api/chat/history api_latency_ms=52.008 status_code=200
[2026-07-31T16:28:04.386874] event=request_completed timestamp=2026-07-31T16:28:04.386874 request_id=53396a39-90a0-4aa4-8a9b-29dddea2eec3 path=/api/files api_latency_ms=56.875 status_code=200
[2026-07-31T16:28:04.391896] event=request_completed timestamp=2026-07-31T16:28:04.391896 request_id=c025e6ed-900d-4064-bafa-d3182c9bca30 path=/api/health api_latency_ms=18.713 status_code=200
[2026-07-31T16:28:04.426395] event=request_completed timestamp=2026-07-31T16:28:04.426395 request_id=25ec08d8-bf6a-416b-8199-0b17348c8919 path=/api/chat/history api_latency_ms=18.689 status_code=200
[2026-07-31T16:28:04.431934] event=request_completed timestamp=2026-07-31T16:28:04.431934 request_id=29db694b-b366-4ebe-b9a8-2efcb05a0d73 path=/api/files api_latency_ms=17.962 status_code=200
[2026-07-31T16:28:09.604990] event=request_completed timestamp=2026-07-31T16:28:09.604990 request_id=be0441b7-2b54-425f-9290-20e104c55f96 path=/api/analytics api_latency_ms=20.149 status_code=200
[2026-07-31T16:44:28.312095] event=[init_db] Database initialized successfully. timestamp=2026-07-31T16:44:28.312095 request_id=None
[2026-07-31T16:45:00.410191] event=[init_db] Database initialized successfully. timestamp=2026-07-31T16:45:00.410191 request_id=None
[2026-07-31T16:51:12.347177] event=[init_db] Database initialized successfully. timestamp=2026-07-31T16:51:12.347177 request_id=None
[2026-07-31T16:51:29.974802] event=request_completed timestamp=2026-07-31T16:51:29.974802 request_id=2c5d41c7-12c5-4e49-b5f6-acaea4b4b468 path=/api/health api_latency_ms=10.41 status_code=200
[2026-07-31T16:51:29.989826] event=request_completed timestamp=2026-07-31T16:51:29.989826 request_id=556a8cb6-a02b-4123-9415-a782943c99e5 path=/api/health api_latency_ms=25.434 status_code=200
[2026-07-31T16:51:30.009317] event=request_completed timestamp=2026-07-31T16:51:30.009317 request_id=f952bb9f-db7d-44f4-92c8-70ce794463fb path=/api/chat/history api_latency_ms=44.925 status_code=200
[2026-07-31T16:51:30.013506] event=request_completed timestamp=2026-07-31T16:51:30.013506 request_id=d043212b-0687-4b85-a225-a1c97609b95d path=/api/files api_latency_ms=47.923 status_code=200
[2026-07-31T16:51:30.016666] event=request_completed timestamp=2026-07-31T16:51:30.016666 request_id=b3256d2a-3122-4ed9-819f-a5dedff8d8f8 path=/api/chat/history api_latency_ms=52.274 status_code=200
[2026-07-31T16:51:30.020204] event=request_completed timestamp=2026-07-31T16:51:30.021624 request_id=0b11e013-a483-442a-b5a0-2c055af2bb7e path=/api/files api_latency_ms=55.812 status_code=200
[2026-07-31T16:51:58.922998] event=[init_db] Database initialized successfully. timestamp=2026-07-31T16:51:58.922998 request_id=None
[2026-07-31T16:52:16.661812] event=request_completed timestamp=2026-07-31T16:52:16.661812 request_id=5e0b202a-a76a-4b77-b843-dfab1427facd path=/api/files api_latency_ms=15.94 status_code=200
[2026-07-31T17:01:37.580066] event=[init_db] Database initialized successfully. timestamp=2026-07-31T17:01:37.580066 request_id=None
[2026-07-31T17:02:12.802599] event=chat_completed timestamp=2026-07-31T17:02:12.802599 retrieval_latency_ms=0.0 llm_latency_ms=0.0 chunk_count=1 user_id=1 request_id=None
[2026-07-31T17:02:14.490536] event=[Chat] Gemini service unavailable: Gemini service is temporarily unavailable timestamp=2026-07-31T17:02:14.490536 request_id=b7d3a023-e53d-4ccc-ad0f-4e6b51bc703c
[2026-07-31T17:02:14.491528] event=request_completed timestamp=2026-07-31T17:02:14.491528 request_id=b7d3a023-e53d-4ccc-ad0f-4e6b51bc703c path=/api/chat api_latency_ms=7.043 status_code=503
[2026-07-31T17:02:14.511058] event=contextual_event timestamp=2026-07-31T17:02:14.511058 message=boom request_id=req-3
[2026-07-31T17:04:53.557505] event=request_completed timestamp=2026-07-31T17:04:53.557505 request_id=4e0327f6-a98f-4bff-bf99-e82ec97f4788 path=/api/health api_latency_ms=11.517 status_code=200
[2026-07-31T17:04:53.577351] event=request_completed timestamp=2026-07-31T17:04:53.578361 request_id=f799d4d2-3222-4ef6-8f6c-bf4ecfd2427b path=/api/files api_latency_ms=34.391 status_code=200
[2026-07-31T17:04:53.582361] event=request_completed timestamp=2026-07-31T17:04:53.582361 request_id=73fbb09d-e40d-42cc-b6c0-3c8609a5713f path=/api/health api_latency_ms=6.012 status_code=200
[2026-07-31T17:04:53.584539] event=request_completed timestamp=2026-07-31T17:04:53.584539 request_id=3e7a2e5f-f2a0-43c8-aa62-e622d8fb2c8e path=/api/chat/history api_latency_ms=36.56 status_code=200
[2026-07-31T17:04:53.609948] event=request_completed timestamp=2026-07-31T17:04:53.609948 request_id=191580bb-2119-4009-bf57-6240ad53ec76 path=/api/files api_latency_ms=17.074 status_code=200
[2026-07-31T17:04:53.614459] event=request_completed timestamp=2026-07-31T17:04:53.614459 request_id=e6510df9-8a4f-44dc-8357-20a6ff9b92bb path=/api/chat/history api_latency_ms=13.019 status_code=200
[2026-07-31T17:04:57.132364] event=request_completed timestamp=2026-07-31T17:04:57.132364 request_id=fcd8fa8b-9326-4ce5-a022-237ce9025884 path=/api/health api_latency_ms=5.011 status_code=200
[2026-07-31T17:04:57.144062] event=request_completed timestamp=2026-07-31T17:04:57.144062 request_id=17199eac-3ba2-476f-93f9-4c9a39591565 path=/api/chat/history api_latency_ms=15.696 status_code=200
[2026-07-31T17:04:57.148057] event=request_completed timestamp=2026-07-31T17:04:57.149058 request_id=ed0ccdae-939f-4336-a3cc-7ec2efa485d4 path=/api/health api_latency_ms=0.999 status_code=200
[2026-07-31T17:04:57.160114] event=request_completed timestamp=2026-07-31T17:04:57.160114 request_id=f7638d22-669c-4357-a7b6-938272588f32 path=/api/files api_latency_ms=32.761 status_code=200
[2026-07-31T17:04:57.181173] event=request_completed timestamp=2026-07-31T17:04:57.181173 request_id=a673a60e-33bf-4b45-8fd8-9d033a1678e8 path=/api/chat/history api_latency_ms=24.05 status_code=200
[2026-07-31T17:04:57.193358] event=request_completed timestamp=2026-07-31T17:04:57.193358 request_id=c0732e13-195a-4fef-a883-40dde064eb0d path=/api/files api_latency_ms=14.176 status_code=200
[2026-07-31T17:05:15.750776] event=request_completed timestamp=2026-07-31T17:05:15.750776 request_id=e28327fa-1f1e-4dbd-9673-4ddcceddc39f path=/api/upload api_latency_ms=3541.133 status_code=200
[2026-07-31T17:05:15.764769] event=request_completed timestamp=2026-07-31T17:05:15.764769 request_id=7ed8009a-ac3e-4b1f-b438-6715f4f79b8a path=/api/files api_latency_ms=5.191 status_code=200
[2026-07-31T17:05:31.961169] event=[DeleteFile] File 5 deleted successfully at 2026-07-31T17:05:31.961169 timestamp=2026-07-31T17:05:31.961169 request_id=85a95f60-fbae-489b-9193-93f1d2018c00
[2026-07-31T17:05:37.475444] event=request_completed timestamp=2026-07-31T17:05:37.475444 request_id=85a95f60-fbae-489b-9193-93f1d2018c00 path=/api/files/5 api_latency_ms=5535.932 status_code=200
[2026-07-31T17:06:24.749137] event=request_completed timestamp=2026-07-31T17:06:24.749137 request_id=e42eb989-3aa6-4f74-aa4e-b5893dd6793a path=/api/chat/stream api_latency_ms=5.998 status_code=200
[2026-07-31T17:06:29.238617] event=chat_completed timestamp=2026-07-31T17:06:29.238617 retrieval_latency_ms=0.022 llm_latency_ms=4.47 chunk_count=3 user_id=5 request_id=None
[2026-07-31T17:08:32.191458] event=[init_db] Database initialized successfully. timestamp=2026-07-31T17:08:32.191458 request_id=None
[2026-07-31T17:08:56.051702] event=[init_db] Database initialized successfully. timestamp=2026-07-31T17:08:56.051702 request_id=None
[2026-07-31T17:09:06.149918] event=[init_db] Database initialized successfully. timestamp=2026-07-31T17:09:06.150918 request_id=None
[2026-07-31T17:09:25.402089] event=chat_completed timestamp=2026-07-31T17:09:25.402089 retrieval_latency_ms=0.0 llm_latency_ms=0.0 chunk_count=1 user_id=1 request_id=None
[2026-07-31T17:09:26.982758] event=[Chat] Gemini service unavailable: Gemini service is temporarily unavailable timestamp=2026-07-31T17:09:26.982758 request_id=e148de1d-ab9b-401a-b2ab-99c12a82d449
[2026-07-31T17:09:26.983765] event=request_completed timestamp=2026-07-31T17:09:26.983765 request_id=e148de1d-ab9b-401a-b2ab-99c12a82d449 path=/api/chat api_latency_ms=5.546 status_code=503
[2026-07-31T17:09:26.996415] event=contextual_event timestamp=2026-07-31T17:09:26.996415 message=boom request_id=req-3
[2026-07-31T17:11:17.792163] event=[init_db] Database initialized successfully. timestamp=2026-07-31T17:11:17.792163 request_id=None
[2026-07-31T17:11:40.288515] event=[init_db] Database initialized successfully. timestamp=2026-07-31T17:11:40.288515 request_id=None
[2026-07-31T17:13:08.957137] event=[init_db] Database initialized successfully. timestamp=2026-07-31T17:13:08.957137 request_id=None
[2026-07-31T17:13:41.628637] event=request_completed timestamp=2026-07-31T17:13:41.628637 request_id=bfde8b3e-0e89-4dde-a99d-f4d7d8d8f6a1 path=/api/upload api_latency_ms=14205.255 status_code=200
[2026-07-31T17:13:41.642478] event=request_completed timestamp=2026-07-31T17:13:41.642478 request_id=e12701e0-a5e4-48f5-bcfd-d391e8f75139 path=/api/files api_latency_ms=5.225 status_code=200
[2026-07-31T17:13:59.129615] event=request_completed timestamp=2026-07-31T17:13:59.129615 request_id=43b43f9a-0cee-4e3e-a3be-50637b264429 path=/api/health api_latency_ms=5.618 status_code=200
[2026-07-31T17:13:59.145528] event=request_completed timestamp=2026-07-31T17:13:59.145528 request_id=0ea5c914-2897-448d-bf8a-d35b91916e44 path=/api/chat/history api_latency_ms=21.531 status_code=200
[2026-07-31T17:13:59.148064] event=request_completed timestamp=2026-07-31T17:13:59.149074 request_id=543e9f8f-0737-487a-b8ac-79ede6e0d409 path=/api/files api_latency_ms=25.107 status_code=200
[2026-07-31T17:13:59.151074] event=request_completed timestamp=2026-07-31T17:13:59.151074 request_id=eb87f335-cc6c-42e9-bd3f-e24399a4e5b4 path=/api/health api_latency_ms=9.079 status_code=200
[2026-07-31T17:13:59.171755] event=request_completed timestamp=2026-07-31T17:13:59.171755 request_id=b01fce27-f907-420a-a3ec-68f0494fd62b path=/api/chat/history api_latency_ms=13.566 status_code=200
[2026-07-31T17:13:59.184288] event=request_completed timestamp=2026-07-31T17:13:59.184288 request_id=4ad90ce5-2d69-477e-a4d5-c42d59339551 path=/api/files api_latency_ms=21.056 status_code=200
[2026-07-31T17:15:54.038024] event=request_completed timestamp=2026-07-31T17:15:54.038024 request_id=56f39392-d479-4903-bc7c-839d08e51ad0 path=/api/analytics api_latency_ms=22.341 status_code=200
[2026-07-31T17:17:59.177662] event=request_completed timestamp=2026-07-31T17:17:59.177662 request_id=5d6af99d-fae8-4b10-93d0-7a5491042353 path=/api/chat/history api_latency_ms=4.598 status_code=200
[2026-07-31T17:18:07.178680] event=request_completed timestamp=2026-07-31T17:18:07.178680 request_id=a8bb1024-8bc6-4dc8-9ecb-b05bf6dff794 path=/api/chat/history api_latency_ms=5.228 status_code=200
[2026-07-31T17:19:15.877902] event=request_completed timestamp=2026-07-31T17:19:15.877902 request_id=9dd8147a-f4aa-4b92-8389-42cea2657b05 path=/api/health api_latency_ms=5.605 status_code=200
[2026-07-31T17:19:15.890918] event=request_completed timestamp=2026-07-31T17:19:15.890918 request_id=985a8c8b-0a33-4366-848d-cfa0f444dbf1 path=/api/chat/history api_latency_ms=18.621 status_code=200
[2026-07-31T17:19:15.894921] event=request_completed timestamp=2026-07-31T17:19:15.894921 request_id=86497322-65f9-4532-969e-6e3c8ce361f0 path=/api/health api_latency_ms=5.019 status_code=200
[2026-07-31T17:19:15.898435] event=request_completed timestamp=2026-07-31T17:19:15.898435 request_id=8a19f04c-ef6d-4cb1-b9a2-59599e38af51 path=/api/files api_latency_ms=27.188 status_code=200
[2026-07-31T17:19:15.914467] event=request_completed timestamp=2026-07-31T17:19:15.914467 request_id=8dd0a3a5-fe23-4434-99a8-066d68a0f14f path=/api/chat/history api_latency_ms=11.029 status_code=200
[2026-07-31T17:19:15.921526] event=request_completed timestamp=2026-07-31T17:19:15.921526 request_id=1a04b40e-7548-4d69-8f44-b495d2a0483a path=/api/files api_latency_ms=11.057 status_code=200
[2026-07-31T17:19:44.082918] event=[init_db] Database initialized successfully. timestamp=2026-07-31T17:19:44.082918 request_id=None
[2026-07-31T17:20:01.004955] event=request_completed timestamp=2026-07-31T17:20:01.004955 request_id=081bdae6-e9fa-452c-95ed-10842d5a9885 path=/api/health api_latency_ms=17.049 status_code=200
[2026-07-31T17:20:01.025566] event=request_completed timestamp=2026-07-31T17:20:01.025566 request_id=e7d559bb-d09e-42dd-ab5a-9af8ec2c4491 path=/api/chat/history api_latency_ms=37.66 status_code=200
[2026-07-31T17:20:01.029078] event=request_completed timestamp=2026-07-31T17:20:01.029078 request_id=9c7b8db2-597e-40d8-8cfe-8ea307132d20 path=/api/health api_latency_ms=7.503 status_code=200
[2026-07-31T17:20:01.034078] event=request_completed timestamp=2026-07-31T17:20:01.034078 request_id=88b629e7-ba0e-450a-8d2d-97b847b14a12 path=/api/files api_latency_ms=47.704 status_code=200
[2026-07-31T17:20:01.046086] event=request_completed timestamp=2026-07-31T17:20:01.046086 request_id=4f7d27cd-57ac-4e1a-a3e5-f291016e0ea8 path=/api/chat/history api_latency_ms=9.996 status_code=200
[2026-07-31T17:20:01.052602] event=request_completed timestamp=2026-07-31T17:20:01.052602 request_id=cd5c1fe2-74ee-4ee1-b8e4-d30451fce0ff path=/api/files api_latency_ms=11.04 status_code=200
[2026-07-31T17:23:01.059060] event=request_completed timestamp=2026-07-31T17:23:01.059060 request_id=1ed78a87-4e77-4795-93c0-a6b95ecf4660 path=/api/health api_latency_ms=5.993 status_code=200
[2026-07-31T17:23:01.076662] event=request_completed timestamp=2026-07-31T17:23:01.076662 request_id=74113855-d65d-4a81-b919-29a5e76ca1a2 path=/api/chat/history api_latency_ms=23.595 status_code=200
[2026-07-31T17:23:01.083686] event=request_completed timestamp=2026-07-31T17:23:01.083686 request_id=7fd87974-4dc6-4ea2-a6be-6504af71dcf3 path=/api/files api_latency_ms=31.626 status_code=200
[2026-07-31T17:23:01.086213] event=request_completed timestamp=2026-07-31T17:23:01.086213 request_id=a27519f6-b789-4b47-852b-10ff485c6b1f path=/api/health api_latency_ms=11.561 status_code=200
[2026-07-31T17:23:01.110978] event=request_completed timestamp=2026-07-31T17:23:01.110978 request_id=e26f8a3f-93fa-4864-99ce-c5e74ab9ea3a path=/api/chat/history api_latency_ms=18.756 status_code=200
[2026-07-31T17:23:01.122138] event=request_completed timestamp=2026-07-31T17:23:01.122138 request_id=5167c4c1-f3e3-4a7f-ac3e-46aaf801f4c7 path=/api/files api_latency_ms=18.172 status_code=200
[2026-07-31T17:23:30.098124] event=[init_db] Database initialized successfully. timestamp=2026-07-31T17:23:30.098124 request_id=None
[2026-07-31T17:23:48.257298] event=request_completed timestamp=2026-07-31T17:23:48.257298 request_id=ae1f812b-661f-4b92-b87c-7c2c620a75b5 path=/api/health api_latency_ms=11.57 status_code=200
[2026-07-31T17:23:48.278604] event=request_completed timestamp=2026-07-31T17:23:48.278604 request_id=6e476be6-8bc3-4eea-86ed-7417b8991521 path=/api/chat/history api_latency_ms=32.876 status_code=200
[2026-07-31T17:23:48.282135] event=request_completed timestamp=2026-07-31T17:23:48.282135 request_id=819b4bda-fa5b-4019-ab49-7e98a897a3e6 path=/api/health api_latency_ms=9.048 status_code=200
[2026-07-31T17:23:48.285577] event=request_completed timestamp=2026-07-31T17:23:48.286157 request_id=e04524f7-7e99-43e5-9eba-a39f91bd2e20 path=/api/files api_latency_ms=40.812 status_code=200
[2026-07-31T17:23:48.305106] event=request_completed timestamp=2026-07-31T17:23:48.305106 request_id=509bd53c-3aa6-49b9-9c66-7c8c718eaaa6 path=/api/chat/history api_latency_ms=13.214 status_code=200
[2026-07-31T17:23:48.308624] event=request_completed timestamp=2026-07-31T17:23:48.308624 request_id=7f2d3e7d-034e-45d6-a0d5-15404038fa58 path=/api/files api_latency_ms=11.068 status_code=200
[2026-07-31T17:23:53.991690] event=request_completed timestamp=2026-07-31T17:23:53.991690 request_id=8bab7408-afd2-4933-8fb0-e7e2340d6ee7 path=/api/health api_latency_ms=4.797 status_code=200
[2026-07-31T17:23:54.000279] event=request_completed timestamp=2026-07-31T17:23:54.000279 request_id=45bad6f3-8705-4077-bc8d-fdedcf821391 path=/api/chat/history api_latency_ms=14.391 status_code=200
[2026-07-31T17:23:54.008747] event=request_completed timestamp=2026-07-31T17:23:54.008747 request_id=6483176f-e114-4439-9c1d-99f7cd1b17c5 path=/api/health api_latency_ms=5.967 status_code=200
[2026-07-31T17:23:54.015310] event=request_completed timestamp=2026-07-31T17:23:54.015310 request_id=8207cecd-997e-4e57-a34c-d68d8ffa267d path=/api/files api_latency_ms=29.422 status_code=200
[2026-07-31T17:23:54.024431] event=request_completed timestamp=2026-07-31T17:23:54.024431 request_id=efe4212c-08f6-473b-8a12-2e09450b0625 path=/api/chat/history api_latency_ms=10.156 status_code=200
[2026-07-31T17:23:54.035973] event=request_completed timestamp=2026-07-31T17:23:54.035973 request_id=a9a3d1e7-16d8-4205-9f22-351fce1a3b15 path=/api/files api_latency_ms=7.539 status_code=200
[2026-07-31T17:25:41.716288] event=request_completed timestamp=2026-07-31T17:25:41.716288 request_id=736a7f03-8ce1-4371-a342-680241cdf0cc path=/api/health api_latency_ms=9.556 status_code=200
[2026-07-31T17:25:41.726485] event=request_completed timestamp=2026-07-31T17:25:41.726485 request_id=23bca970-27f6-43d4-9a83-96c0db8f252d path=/api/chat/history api_latency_ms=19.753 status_code=200
[2026-07-31T17:25:41.732565] event=request_completed timestamp=2026-07-31T17:25:41.732565 request_id=38cb705f-3a21-41d0-91aa-b8efef6eeca3 path=/api/files api_latency_ms=26.844 status_code=200
[2026-07-31T17:25:41.736303] event=request_completed timestamp=2026-07-31T17:25:41.736303 request_id=58d34f8a-27a0-429b-b90a-7c7b471e944d path=/api/health api_latency_ms=9.818 status_code=200
[2026-07-31T17:25:41.758129] event=request_completed timestamp=2026-07-31T17:25:41.758129 request_id=a2801402-b94a-4e6f-af42-affc0c2cab78 path=/api/chat/history api_latency_ms=17.848 status_code=200
[2026-07-31T17:25:41.763289] event=request_completed timestamp=2026-07-31T17:25:41.763289 request_id=75f426f6-f6eb-48d4-a46e-3d84d8561f6b path=/api/files api_latency_ms=20.476 status_code=200
[2026-07-31T17:25:59.561080] event=[DeleteFile] File 4 deleted successfully at 2026-07-31T17:25:59.561080 timestamp=2026-07-31T17:25:59.561080 request_id=6207a08d-a0fc-44d3-8312-deb86d32b88c
[2026-07-31T17:26:05.339988] event=request_completed timestamp=2026-07-31T17:26:05.339988 request_id=6207a08d-a0fc-44d3-8312-deb86d32b88c path=/api/files/4 api_latency_ms=5809.537 status_code=200
[2026-07-31T17:28:03.322298] event=request_completed timestamp=2026-07-31T17:28:03.322298 request_id=6c0f6588-1c8a-4d40-a533-7656b027db1a path=/api/analytics api_latency_ms=18.733 status_code=200
[2026-07-31T17:36:25.653644] event=[init_db] Database initialized successfully. timestamp=2026-07-31T17:36:25.653644 request_id=None
[2026-07-31T17:36:53.954226] event=[init_db] Database initialized successfully. timestamp=2026-07-31T17:36:53.954226 request_id=None
[2026-07-31T17:38:48.208267] event=[init_db] Database initialized successfully. timestamp=2026-07-31T17:38:48.209229 request_id=None
[2026-07-31T17:39:04.030358] event=request_completed timestamp=2026-07-31T17:39:04.030358 request_id=352beedd-1eef-4a4d-8d9d-cfd90124632c path=/api/health api_latency_ms=6.516 status_code=200
[2026-07-31T17:39:04.074734] event=request_completed timestamp=2026-07-31T17:39:04.074734 request_id=2ee40b02-c8fc-4f8e-b4df-6672fcee6866 path=/api/health api_latency_ms=4.515 status_code=200
[2026-07-31T17:39:04.083054] event=request_completed timestamp=2026-07-31T17:39:04.083054 request_id=d71bfd16-776c-4159-bc3a-e766b0ea1a7b path=/api/chat/history api_latency_ms=59.212 status_code=200
[2026-07-31T17:39:04.085879] event=request_completed timestamp=2026-07-31T17:39:04.085879 request_id=072c8261-3408-409f-a597-3e0f58ab43e1 path=/api/files api_latency_ms=62.037 status_code=200
[2026-07-31T17:39:04.102045] event=request_completed timestamp=2026-07-31T17:39:04.102045 request_id=1de6ad9a-a589-4d24-b7de-07b013ccc789 path=/api/chat/history api_latency_ms=11.281 status_code=200
[2026-07-31T17:39:04.107317] event=request_completed timestamp=2026-07-31T17:39:04.107317 request_id=b6a5abd9-c311-4e5c-bbdb-cbae7f8ddd0e path=/api/files api_latency_ms=11.277 status_code=200
[2026-07-31T17:39:07.744521] event=request_completed timestamp=2026-07-31T17:39:07.744521 request_id=0b462e79-2f75-4695-aff0-17547013baba path=/api/health api_latency_ms=5.517 status_code=200
[2026-07-31T17:39:07.755580] event=request_completed timestamp=2026-07-31T17:39:07.755580 request_id=bb01626f-69cb-40d9-876f-eeaa5e666158 path=/api/chat/history api_latency_ms=16.576 status_code=200
[2026-07-31T17:39:07.764433] event=request_completed timestamp=2026-07-31T17:39:07.764433 request_id=bc9ec1b5-4719-4347-a91a-de4c7cea4ac3 path=/api/health api_latency_ms=5.848 status_code=200
[2026-07-31T17:39:07.770622] event=request_completed timestamp=2026-07-31T17:39:07.770622 request_id=23c31fdd-a5c1-4265-8818-179f97ca650b path=/api/files api_latency_ms=32.633 status_code=200
[2026-07-31T17:39:07.785147] event=request_completed timestamp=2026-07-31T17:39:07.785147 request_id=f8371359-6202-4a9a-95ec-1f4309f057b6 path=/api/chat/history api_latency_ms=17.042 status_code=200
[2026-07-31T17:39:07.797129] event=request_completed timestamp=2026-07-31T17:39:07.797129 request_id=fb6bb3e4-da1a-4b37-a1ca-85196f925f6e path=/api/files api_latency_ms=13.499 status_code=200
[2026-07-31T17:44:37.354104] event=[init_db] Database initialized successfully. timestamp=2026-07-31T17:44:37.354104 request_id=None
[2026-07-31T17:44:55.302513] event=request_completed timestamp=2026-07-31T17:44:55.302513 request_id=f4ac6bf6-9efe-4210-a527-6d11ed5a4d02 path=/api/health api_latency_ms=12.252 status_code=200
[2026-07-31T17:44:55.317709] event=request_completed timestamp=2026-07-31T17:44:55.317709 request_id=1d16e2cc-af77-41cb-b4c7-2664d8f280c8 path=/api/files api_latency_ms=28.44 status_code=200
[2026-07-31T17:44:55.321331] event=request_completed timestamp=2026-07-31T17:44:55.321331 request_id=c22f6378-e163-41ec-8c3c-7d4c28abd3df path=/api/health api_latency_ms=8.624 status_code=200
[2026-07-31T17:44:55.324883] event=request_completed timestamp=2026-07-31T17:44:55.324883 request_id=59fada30-b0e7-486b-83d7-567a652aa55a path=/api/chat/history api_latency_ms=33.714 status_code=200
[2026-07-31T17:44:55.335482] event=request_completed timestamp=2026-07-31T17:44:55.335482 request_id=e7f765d9-f797-4a5a-a50e-5a77d6153988 path=/api/files api_latency_ms=7.605 status_code=200
[2026-07-31T17:44:55.341138] event=request_completed timestamp=2026-07-31T17:44:55.341138 request_id=dcc31c96-aa8c-416e-a910-8f6b77789cda path=/api/chat/history api_latency_ms=8.709 status_code=200
[2026-07-31T17:45:26.460974] event=request_completed timestamp=2026-07-31T17:45:26.460974 request_id=2099c4d9-771c-4a0e-91b0-7a25faf86d37 path=/api/analytics api_latency_ms=20.076 status_code=200
[2026-07-31T17:47:49.166063] event=request_completed timestamp=2026-07-31T17:47:49.166063 request_id=85a0313c-e950-4377-a47e-cde4b397e640 path=/api/chat/stream api_latency_ms=5.529 status_code=200
[2026-07-31T17:47:51.401405] event=chat_completed timestamp=2026-07-31T17:47:51.401405 retrieval_latency_ms=0.251 llm_latency_ms=1.98 chunk_count=2 user_id=5 request_id=None
[2026-07-31T17:48:05.119003] event=request_completed timestamp=2026-07-31T17:48:05.119003 request_id=6e8e2740-eff7-48a5-ad16-dca89b42c625 path=/api/chat/stream api_latency_ms=3.011 status_code=200
[2026-07-31T17:48:07.056144] event=chat_completed timestamp=2026-07-31T17:48:07.056144 retrieval_latency_ms=0.014 llm_latency_ms=1.92 chunk_count=3 user_id=5 request_id=None
[2026-07-31T17:48:13.580057] event=request_completed timestamp=2026-07-31T17:48:13.580057 request_id=0a0e3652-a752-4b52-a9da-621755473634 path=/api/chat/stream api_latency_ms=4.592 status_code=200
[2026-07-31T17:48:15.671395] event=chat_completed timestamp=2026-07-31T17:48:15.671395 retrieval_latency_ms=0.016 llm_latency_ms=2.07 chunk_count=4 user_id=5 request_id=None
