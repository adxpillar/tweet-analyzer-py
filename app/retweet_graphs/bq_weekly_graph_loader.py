

from app.retweet_graphs.bq_weekly_grapher import BigQueryWeeklyRetweetGrapher

if __name__ == "__main__":

    storage_service = BigQueryWeeklyRetweetGrapher.init_storage_service()

    graph = storage_service.load_graph() # will print a memory profile...

    storage_service.report(graph) # will print graph size
