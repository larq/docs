from keras_autodoc import DocumentationGenerator, get_classes, get_functions

repo_apis = {
    "larq": {
        "layers.md": [
            "larq.layers.QuantDense",
            "larq.layers.QuantConv1D",
            "larq.layers.QuantConv2D",
            "larq.layers.QuantConv3D",
            "larq.layers.QuantDepthwiseConv2D",
            "larq.layers.QuantSeparableConv1D",
            "larq.layers.QuantSeparableConv2D",
            "larq.layers.QuantConv2DTranspose",
            "larq.layers.QuantConv3DTranspose",
            "larq.layers.QuantLocallyConnected1D",
            "larq.layers.QuantLocallyConnected2D",
        ],
        "activations.md": get_classes("larq.activations"),
        "callbacks.md": get_classes("larq.constraints"),
        "constraints.md": get_classes("larq.constraints"),
        "context.md": get_classes("larq.context"),
        "optimizers.md": get_classes("larq.optimizers"),
        "math.md": get_functions("larq.math"),
        # "models.md": ["larq.models.summary"],  #  parse error, suspecting `print`
        "metrics.md": get_classes("larq.metrics"),
        "quantizers.md": get_classes("larq.quantizers"),
    },
    "zoo": {
        "index.md": ["larq_zoo.decode_predictions", "larq_zoo.preprocess_input"],
        "literature.md": [
            "larq_zoo.literature.BinaryAlexNet",
            "larq_zoo.literature.BiRealNet",
            "larq_zoo.literature.BinaryResNetE18",
            "larq_zoo.literature.BinaryDenseNet28",
            "larq_zoo.literature.BinaryDenseNet37",
            "larq_zoo.literature.BinaryDenseNet37Dilated",
            "larq_zoo.literature.BinaryDenseNet45",
            "larq_zoo.literature.DoReFaNet",
            "larq_zoo.literature.XNORNet",
        ],
        "sota.md": [
            "larq_zoo.sota.QuickNet",
            "larq_zoo.sota.QuickNetLarge",
            "larq_zoo.sota.QuickNetXL",
        ],
    },
    "compute-engine": {"index.md": ["larq_compute_engine.convert_keras_model"]},
}

for repo, api_pages in repo_apis.items():
    doc_generator = DocumentationGenerator(api_pages)
    doc_generator.generate(f"./docs/{repo}/api")
