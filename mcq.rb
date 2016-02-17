require 'yaml'
require 'pathname'

week = '03'
file = "mcq_#{week}.yml"
exit unless Pathname(file).exist?
mcqs = YAML.load_file(file)

header_template = """
Multiple Choice Questions
=============================================
"""

mcqs = mcqs.each_with_index.map do |mcq, mcq_index|

  mcq = Hash[mcq.map { | (k,v) | [k.to_sym, v] } ]

  mcq_number = mcq_index + 1

  multi = mcq[:answer].is_a?(Array) ? '-mc' : ''

  mcq_template = """
  .. eqt#{multi}:: mcq-#{week}-#{mcq_number}

     **Question #{mcq_number}** #{mcq[:question]}
  """

  if mcq[:image]
    image_template = """
     .. figure:: /Images/#{mcq[:image]}
    """

    mcq_template += image_template
  end

  options = mcq[:options].each_with_index.map do |option, option_index|

    carrier = option_index.zero? ? 'A' : '#'

    letter  = (65 + option_index).chr

    if mcq[:answer].is_a?(Array)
      correct = mcq[:answer].include?(letter) ? 'C' : 'I'
    else
      correct = letter == mcq[:answer] ? 'C' : 'I'
    end

    option  = option.to_s.capitalize
    option  = option.gsub(/[\n|\s|\.]$/, '')

    """
     #{carrier}) :eqt:`#{correct}` #{option}
    """

  end

  options = options.join('')
  mcq_template + options

end

data = header_template + mcqs.join('')

file = "Week_#{week}/page_07.rst"
File.write(file, data)
