from masonite.routes import Route

ROUTES = [
    Route.get("/", "WelcomeController@show").name("welcome"),
    Route.get("/health", "InsightController@health"),
    Route.post("/ingest/social-post", "InsightController@ingest_social_post"),

    Route.post("/insights/rank", "InsightController@rank_complaints"),
    Route.get("/insights/demo", "InsightController@demo_insights"),
    Route.get("/insights/summary", "InsightController@summary"),
    Route.get("/insights/trends", "InsightController@trends"),
    Route.get("/insights/issues", "InsightController@issues"),
    Route.get("/insights/issue-clusters", "InsightController@issue_clusters"),
    Route.get("/insights/alerts", "InsightController@alerts"),
]
