from conans import ConanFile, CMake, tools


class FastDDSConan(ConanFile):
    name = "Fast-DDS-RPC"
    version = "1.0.0"
    license = "Apache License 2.0"
    author = "Frieder Pankratz"
    url = "https://github.com/TUM-CONAN/conan-fast-dds-rpc.git"
    description = "Conan wrapper for Fast-DDS-RPC"    
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "Build_Java" : [True, False]}
    default_options = {"shared": True, "Build_Java" : False } #, "RPCProto" : "rpcdds"}
    generators = "cmake"

    requires = ("Fast-DDS/2.0.0@camposs/stable","Boost/1.72.0@camposs/stable" )
    

    def source(self):
        git = tools.Git()        
        git.clone("https://github.com/FriederPankratz/RPC.git", self.version)

        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        tools.replace_in_file("CMakeLists.txt", "project(\"fastrpc\")",
                              '''project("fastrpc")
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()
''')
        tools.replace_in_file("CMakeLists.txt", "project(\"rpcdds\")",
                              '''project("rpcdds")
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()
''')
        tools.replace_in_file("CMakeLists.txt", "project(\"rpcrest\")",
                              '''project("rpcrest")
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()
''')

    def configure(self):
        if self.options.shared:                                    
            self.options['Fast-DDS'].shared = True            
            self.options['Boost'].shared = True

    def _configure_cmake(self):        
        cmake = CMake(self)
        cmake.verbose = True

        def add_cmake_option(option, value):
            var_name = "{}".format(option).upper()
            value_str = "{}".format(value)
            var_value = "ON" if value_str == 'True' else "OFF" if value_str == 'False' else value_str
            cmake.definitions[var_name] = var_value        

        for option, value in self.options.items():
            add_cmake_option(option, value)

        cmake.configure()
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):        
        self.cpp_info.libs = tools.collect_libs(self)
