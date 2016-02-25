Dir.glob('_build/**/*.html') do |file|
  data = File.read(file)
  data = data.gsub('class="reference external', 'target="_blank" class="reference external')
  File.write(file, data)
end