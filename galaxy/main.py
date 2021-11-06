from .cartography import YoutubeCartographer

if __name__ == "__main__":
    depth = 2
    initial_node = "Np695V8lzeg", "I cracked Youtube Algorithm", "ici Amy Plant"
    ytGraph = YoutubeCartographer(initial_node=initial_node, depth=depth)
    ytGraph.build()
    ytGraph.save(f"iap.{depth}.gexf")
